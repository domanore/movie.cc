from flask import Flask, request, jsonify, render_template_string
from threading import Thread
from queue import Queue
import time

app = Flask(__name__)

# Production configuration
app.config['ENV'] = 'production'

# Simulated database
showtimes = {
    # Showtimes and seat details here
}

# Booking history
booking_history = []

# FIFO Queue for booking requests
booking_queue = Queue()

# Function to process booking requests from the queue
def process_booking_queue():
    while True:
        if not booking_queue.empty():
            booking_request = booking_queue.get()
            response = process_booking(booking_request)
            booking_queue.task_done()
            print(response)
        time.sleep(1)

# Function to process a single booking request
def process_booking(data):
    showtime = data.get('showtime')
    seat = data.get('seat')
    name = data.get('name')
    # Booking logic here
    return {"status": "success", "message": "Seat successfully booked!", "movie": showtimes[showtime]["movie"]}

@app.route('/')
def index():
    showtimes_html = generate_showtimes_html()
    history_html = generate_history_html()
    return render_template_string('''...''', showtimes_html=showtimes_html, history_html=history_html)

def generate_showtimes_html():
    showtimes_html = ""
    for showtime, details in showtimes.items():
        seats_html = generate_seats_html(showtime)
        showtimes_html += f'''
        <div class="showtime" data-formation="{details["formation"]}">
            <h3>{details["movie"]}</h3>
            <p>{showtime}</p>
            <div class="seat-plan">
                {seats_html}
            </div>
            <button class="select-button" onclick="this.nextElementSibling.style.display = 'flex'">Select Seats</button>
        </div>
        '''
    return showtimes_html

def generate_seats_html(showtime):
    seats_html = ""
    seats = showtimes[showtime]["seats"]
    for row in "ABCDE":
        seats_html += '<div class="seat-row">'
        for num in range(1, 11):
            seat = f"{row}{num}"
            disabled = "disabled" if not seats[seat] else ""
            seats_html += f'<button id="{showtime}-{seat}" class="seat" {disabled} onclick="bookSeat(\'{showtime}\', \'{seat}\')">{seat}</button>'
        seats_html += '</div>'
    return seats_html

def generate_history_html():
    history_html = ""
    # Generate booking history HTML here
    return history_html

if __name__ == '__main__':
    # Start the booking queue processing thread
    Thread(target=process_booking_queue, daemon=True).start()
    # Run the Flask app
    app.run(debug=True)
