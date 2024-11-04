import json


class Passenger:
    def __init__(self, name, age, ticket_id):
        self.name = name
        self.age = age
        self.ticket_id = ticket_id
        self.seat_status = "Waiting"  # Initially, all passengers are on the waiting list
        self.food_order = []

    def display_passenger_info(self):
        print(f"Passenger Information:\nName: {self.name}\nAge: {self.age}\n"
              f"Ticket ID: {self.ticket_id}\nSeat Status: {self.seat_status}\n"
              f"Food Orders: {', '.join(self.food_order) if self.food_order else 'None'}")


class Train:
    def __init__(self, train_number, route, total_seats):
        self.train_number = train_number
        self.route = route
        self.total_seats = total_seats
        self.passengers = []
        self.waiting_list = []

    def add_passenger(self, passenger):
        if len(self.passengers) < self.total_seats:
            self.passengers.append(passenger)
            passenger.seat_status = "Confirmed"
        else:
            self.waiting_list.append(passenger)
            passenger.seat_status = "Waiting"
        print(f"Passenger {passenger.name} added to Train {self.train_number}. Seat status: {passenger.seat_status}")

    def confirm_waitlist(self):
        if len(self.passengers) < self.total_seats and self.waiting_list:
            passenger = self.waiting_list.pop(0)
            self.passengers.append(passenger)
            passenger.seat_status = "Confirmed"
            print(f"Passenger {passenger.name} confirmed from waiting list.")

    def display_train_info(self):
        passenger_names = ', '.join(passenger.name for passenger in self.passengers)
        waiting_names = ', '.join(passenger.name for passenger in self.waiting_list)
        print(f"Train Information:\nTrain Number: {self.train_number}\n"
              f"Route: {self.route}\nTotal Seats: {self.total_seats}\n"
              f"Confirmed Passengers: {passenger_names if passenger_names else 'None'}\n"
              f"Waiting List: {waiting_names if waiting_names else 'None'}")


class TrainManagementSystem:
    def __init__(self):
        self.passengers = {}
        self.trains = {}

    def add_passenger(self):
        name = input("Enter Passenger Name: ")
        age = int(input("Enter Passenger Age: "))
        ticket_id = input("Enter Ticket ID: ")

        passenger = Passenger(name, age, ticket_id)
        self.passengers[ticket_id] = passenger
        print(f"Passenger {name} (Ticket ID: {ticket_id}) added successfully.")

    def add_train(self):
        train_number = input("Enter Train Number: ")
        route = input("Enter Train Route: ")
        total_seats = int(input("Enter Total Seats: "))

        train = Train(train_number, route, total_seats)
        self.trains[train_number] = train
        print(f"Train {train_number} (Route: {route}) created with {total_seats} seats.")

    def book_ticket(self):
        ticket_id = input("Enter Ticket ID: ")
        train_number = input("Enter Train Number: ")

        if ticket_id in self.passengers and train_number in self.trains:
            passenger = self.passengers[ticket_id]
            train = self.trains[train_number]
            train.add_passenger(passenger)
        else:
            print("Error: Passenger or Train does not exist.")

    def add_food_order(self):
        ticket_id = input("Enter Ticket ID: ")
        if ticket_id in self.passengers:
            passenger = self.passengers[ticket_id]
            food_item = input("Enter Food Item to Order: ")
            passenger.food_order.append(food_item)
            print(f"Food order '{food_item}' added for passenger {passenger.name}.")
        else:
            print("Error: Passenger does not exist.")

    def display_passenger_details(self):
        ticket_id = input("Enter Ticket ID: ")
        if ticket_id in self.passengers:
            self.passengers[ticket_id].display_passenger_info()
        else:
            print("Error: Passenger does not exist.")

    def display_train_details(self):
        train_number = input("Enter Train Number: ")
        if train_number in self.trains:
            self.trains[train_number].display_train_info()
        else:
            print("Error: Train does not exist.")

    def save_data(self):
        data = {
            "passengers": {ticket_id: {
                "name": passenger.name,
                "age": passenger.age,
                "seat_status": passenger.seat_status,
                "food_order": passenger.food_order
            } for ticket_id, passenger in self.passengers.items()},
            "trains": {train_number: {
                "route": train.route,
                "total_seats": train.total_seats,
                "passengers": [passenger.ticket_id for passenger in train.passengers],
                "waiting_list": [passenger.ticket_id for passenger in train.waiting_list]
            } for train_number, train in self.trains.items()}
        }
        with open('train_data.json', 'w') as f:
            json.dump(data, f)
        print("All passenger and train data saved successfully.")

    def load_data(self):
        try:
            with open('train_data.json', 'r') as f:
                data = json.load(f)
                for ticket_id, passenger_data in data['passengers'].items():
                    passenger = Passenger(passenger_data["name"], passenger_data["age"], ticket_id)
                    passenger.seat_status = passenger_data["seat_status"]
                    passenger.food_order = passenger_data["food_order"]
                    self.passengers[ticket_id] = passenger
                
                for train_number, train_data in data['trains'].items():
                    train = Train(train_number, train_data["route"], train_data["total_seats"])
                    for ticket_id in train_data["passengers"]:
                        if ticket_id in self.passengers:
                            train.add_passenger(self.passengers[ticket_id])
                    for ticket_id in train_data["waiting_list"]:
                        if ticket_id in self.passengers:
                            train.waiting_list.append(self.passengers[ticket_id])
                    self.trains[train_number] = train
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No data file found. Starting with an empty system.")


def main():
    system = TrainManagementSystem()
    system.load_data()

    while True:
        print("\n==== Train Management System ====")
        print("1. Add New Passenger")
        print("2. Add New Train")
        print("3. Book Ticket")
        print("4. Add Food Order for Passenger")
        print("5. Display Passenger Details")
        print("6. Display Train Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")

        option = input("Select Option: ")

        if option == "1":
            system.add_passenger()
        elif option == "2":
            system.add_train()
        elif option == "3":
            system.book_ticket()
        elif option == "4":
            system.add_food_order()
        elif option == "5":
            system.display_passenger_details()
        elif option == "6":
            system.display_train_details()
        elif option == "7":
            system.save_data()
        elif option == "8":
            system.load_data()
        elif option == "0":
            print("Exiting Train Management System. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
