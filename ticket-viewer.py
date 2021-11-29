# Submission by: Siddhanth Jayaraj Ajri

import re
import json
import requests

class TicketViewer:

    def __init__(self):
        # Opening JSON file
        f = open('credentials.json')
        
        # returns JSON object as a dictionary
        data = json.load(f)
        self.subdomain = data["subdomain"]
        self.email = data["email"]
        self.password = data["password"]
        self.token = ""
        self.tickets = []

    def connection_established(self):
        url = 'https://{}.zendesk.com/api/v2/oauth/clients.json'
        
        try:
            response = requests.get(url.format(self.subdomain), auth = (self.email, self.password)).json()
            headers = {
                'Content-Type': 'application/json',
                }
            data = '{"token": {"client_id": "' + str(response['clients'][0]['id']) + '", "scopes": ["read", "write"]}}'
            url1 = 'https://{}.zendesk.com/api/v2/oauth/tokens.json'
            response1 = requests.post(url1.format(self.subdomain), headers = headers, data = data, auth=(self.email, self.password))
            
            self.token = response1.json()['token']['full_token']
        except:
            return False
        
        if self.token:
            return True
        else:
            return False

    def get_all_tickets(self):
        try:
            url = 'https://{}.zendesk.com/api/v2/tickets.json'
            #url = 'https://{}.zendesk.com/api/v2/requests.json'

            headers = {
                'Authorization': 'Bearer {}'.format(self.token),
            }

            response = requests.get(url.format(self.subdomain), headers=headers)
            if (str(response.status_code).strip() == '200'):
                self.tickets = response.json()['tickets']
                return("Successful request\n")
            else:
                return("ERROR : " + str(response.status_code) + "\n")    
        except:
            return("ERROR: " + str(response.status_code) + "\n")

    def view_ticket_list(self):
        """
        Print the tickets page by page, with max page size of 25.
        Return: String output of page with ticket details
        """
        try:
            url = 'https://{}.zendesk.com/api/v2/tickets.json?page[size]=25'
            headers = {
                    'Authorization': 'Bearer {}'.format(self.token),
            }
            while url:
                response = requests.get(url.format(self.subdomain), headers=headers)
                data = response.json()

                for ticket in data['tickets']:
                    print("\nID" + str(ticket['id']))
                    print("Subject: " + ticket['subject'])
                    print("Description: " + ticket['description'])

                if data['meta']['has_more']:
                    inp3 = input("\nShow next page? Press y/Y or else no more pages will be shown.\n")
                    if inp3 == 'y' or inp3 == 'Y':
                        url = data['links']['next']
                    else:
                        print("\nAll pages shown...")
                        return
                else:
                    print("\nAll pages shown...")
                    url = None
            return
        except:
            print("ERROR\n")
            return
        
    def get_ticket_by_id(self, inp):
        """
        Return the ticket with ID requested.
        Parameters:
            input - string ID
        Return: String output of ticket details
        """
        
        try:
            url = 'https://{}.zendesk.com/api/v2/search.json?query={}'
            headers = {
                    'Authorization': 'Bearer {}'.format(self.token),
            }
            response = requests.get(url.format(self.subdomain, inp), headers=headers)
            data = response.json()
            return("ID: " + str(data['results'][0]['id']) + "\nSubject: " + str(data['results'][0]['subject']) + "\nDescription: " + str(data['results'][0]['description']))
        except:
            return("ERROR: " + str(response.status_code) + " - No such ticket found.")

    def __str__(self):
        return "ZCC Ticket Viewer"

def main():
    # Create a new object
    tv = TicketViewer()
    while True:
        inp = input("Welcome to Ticket Viewer! Establish connection? Press y/Y for Yes.\n").strip()
        if (inp == 'y' or inp == 'Y'):
            if tv.connection_established():
                print("Connection Established!\n")
                while True:
                    inp = input("Select options:\n1. Get all tickets\n2. View all tickets as list\n3. Get ticket by ID\n4. Quit\nEnter 1, 2, 3 or 4.\n").strip()
                    if inp in ['1', '2', '3', '4']:
                        print("You chose option " + str(inp) + "\n")
                        if inp == '4':
                            print("Quitting...\n")
                            return
                        if inp == '1':
                            print(tv.get_all_tickets())
                            print("\n")
                        elif inp == '2':
                            tv.view_ticket_list()
                        elif inp == '3':
                            inp1 = input("Enter ticket ID: ")
                            print(tv.get_ticket_by_id(inp1))
                            print()
                    else:
                        print("Wrong input.\n")
            
            else:
                print("No connection established... Try again later")
                return
        else:
            print("Wrong input.")

# This makes it so that the main function only runs when this file
# is directly run and not when it is imported as a module
if __name__ == "__main__":
    main()
