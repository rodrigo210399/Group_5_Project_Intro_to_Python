from flask import Flask, render_template, redirect, url_for, request
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os

app = Flask(__name__)
scheduler = BackgroundScheduler()

# Function to update the list of companies and columns
def update_data():
    # Print a message with the current time when the update is triggered
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Data update triggered at: {current_time}")

    # Get a list of all CSV files in the company_datasets folder
    csv_files = [f for f in os.listdir('update_data/company_datasets') if f.endswith('_data.csv')]

    # Extract company names from CSV filenames
    companies = [filename.split('_data.csv')[0] for filename in csv_files]

    # List of numeric columns to visualize
    columns = ['Last Price', 'Change', 'Percent Change', 'Volume', 'Market Cap']

    # Store the updated data in the app's context
    app.config['companies'] = companies
    app.config['columns'] = columns
    app.config['last_update_time'] = current_time  # Store the time of the last update

# Schedule the data update job every 2 minutes
scheduler.add_job(update_data, 'interval', minutes=1)

# Update data on application startup
update_data()

# Update the 'home' route
@app.route('/')
def home():
    # Retrieve the companies, columns, and current time from the app's context
    companies = app.config.get('companies', [])
    columns = app.config.get('columns', [])

    last_update_time = pd.to_datetime(app.config.get('last_update_time', 'Not available'))
    # Get the current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Print the companies and columns to check the output
    #print("Companies:", companies)
    #print("Columns:", columns)
    if pd.to_datetime('10:00:00') < last_update_time < pd.to_datetime('16:00:00'):
        pass
    else:
        last_update_time = pd.to_datetime('16:00:00')


    # Render the HTML template with the list of companies, columns, last update time, and current time
    return render_template('home.html', companies=companies, columns=columns,
                           last_update_time=last_update_time, current_time=current_time)

# Visualization route (to see the plots)
@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if request.method == 'GET':
        # Get the selected company and column from the query parameters
        company = request.args.get('company', '')
        selected_column = request.args.get('column', 'Last Price')

        # Read the CSV file into a DataFrame
        csv_file_path = f'update_data/company_datasets/{company}_data.csv'
        df = pd.read_csv(csv_file_path)

        df.reset_index(drop=True, inplace=True)

        # Calculate the time difference between each row and the last update time
        last_update_time = pd.to_datetime(app.config.get('last_update_time', 'Not Time Available'))

        if pd.to_datetime('10:00:00') < last_update_time < pd.to_datetime('16:00:00'):
            df['TimeDifference'] = - pd.to_timedelta(df.index.size - df.index.to_series().rank(method='first') , unit='m') + last_update_time
        else:
            df['TimeDifference'] = - pd.to_timedelta(df.index.size - df.index.to_series().rank(method='first') , unit='m') + pd.to_datetime('16:00:00')
        # Sort the DataFrame by TimeDifference
        df['TimeDifference'] = df['TimeDifference'][::-1]

        # Calculate the start time based on the length of the DataFrame
        start_time = last_update_time - len(df)*pd.Timedelta(minutes=1)

        # Create a histogram using Plotly Express instead of a line plot
        #fig = px.histogram(df, x='TimeDifference', y=selected_column, nbins=len(df),
        #                   title=f'{selected_column} Visualization for {df["Name"][0]}')

        # Create a line plot with filled area
        # Create a line trace
        line_trace = go.Scatter(
            x=df['TimeDifference'],
            y=df[selected_column],
            mode='lines',
            name=f'<span style="color:white;">{selected_column} for {df["Name"][0]}</span>'
        )

        # Add an area trace
        area_trace = go.Scatter(
            x=df['TimeDifference'],
            y=df[selected_column],
            fill='tozeroy',
            mode='none',  # 'none' means only fill, no line
            showlegend=False
        )

        # Create the figure
        fig = go.Figure(data=[line_trace, area_trace])

        # Change the line color
        fig.update_traces(marker=dict(color='white'))  # Change 'blue' to your desired color


        # Increase the title font size
        fig.update_layout(title_font_size=34)  # Adjust the size as needed

        # Adjust the bargap and bargroupgap
        fig.update_layout(bargap=0.1, bargroupgap=0.1)

        # Set the layout, title, and axis labels
        fig.update_layout(
            title=f'<span style="color:white; font-size :50px;">{selected_column} for {df["Name"][0]}</span>',  # Set title text color
            xaxis_title='Time Difference',
            yaxis_title=selected_column,
            legend=dict(
                title=dict(text='<span style="color:white;">Legend Title</span>')  # Set legend title text color
            )
        )
        # Update layout to set axis and title text color to white
        fig.update_layout(

            xaxis=dict(tickfont=dict(color='white'), 
                       title=dict(text=f'DateTime', 
                                  font=dict(color='white'))),  # Set x-axis text and label color to white
            yaxis=dict(tickfont=dict(color='white'), 
                       title=dict(text=f'{selected_column}', 
                                  font=dict(color='white'))),  # Set y-axis text and label color to white
            title_font=dict(color='white')  # Set title text color to white
        )

        # Update layout to remove background color
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)'  # Set paper color to transparent
        )

        # Set the x-axis range from start_time to 5 minutes after the last update time
        # Stop the axis updates if the last_update_time is not within 10 and 16 time.
        if pd.to_datetime('10:00:00') < last_update_time < pd.to_datetime('16:00:00'):
            fig.update_xaxes(range=[start_time, last_update_time + pd.Timedelta(minutes=5)])
        else:
            end_time = pd.to_datetime('16:00:00') - (len(df)-1) * pd.Timedelta(minutes=1)
            fig.update_xaxes(range=[end_time, pd.to_datetime('16:00:00')])

        # Set the y-axis range from the 95% below of the minimum value and go upto 5% above the maximum value.
        fig.update_yaxes(range=[.95*min(df[selected_column]), 1.05*max(df[selected_column])])


        fig.update_layout(title_font=dict(family="cursive"))
        # Convert the plot to HTML
        plot_html = pio.to_html(fig, full_html=False)

        # Concise explanation below the plot
        concise_explanation = (f"This plot shows the {selected_column}'s "
                               f"evolution for the company {df['Name'][0]} (Symbol: {company}) "
                               f"for todays data.")

        # Define the allowed columns for the selector
        allowed_columns = ['Last Price', 'Change', 'Percent Change', 'Volume', 'Market Cap']

        # Get the last update time from the app's context
        if pd.to_datetime('10:00:00') < last_update_time < pd.to_datetime('16:00:00'):
            pass
        else:
            last_update_time = pd.to_datetime('16:00:00')

        # Render the HTML template with the plot, concise explanation, selected column, and last update time
        return render_template('visualization.html', plot_html=plot_html,
                               company=company, selected_column=selected_column,
                               concise_explanation=concise_explanation, allowed_columns=allowed_columns,
                               last_update_time=last_update_time)

    # Handle other methods if needed
    return redirect(url_for('home'))

# About route
@app.route('/about')
def about():
    # Retrieve the last update time and current time from the app's context
    last_update_time = pd.to_datetime(app.config.get('last_update_time', 'Not available'))
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if pd.to_datetime('10:00:00') < last_update_time < pd.to_datetime('16:00:00'):
        pass
    else:
        last_update_time = pd.to_datetime('16:00:00')

    # Render the HTML template with the last update time and current time
    return render_template('about.html', last_update_time=last_update_time, current_time=current_time)

if __name__ == '__main__':
    # Start the scheduler
    scheduler.start()
    
    # Run the Flask app
    app.run(debug=True)
