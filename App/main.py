"""Main module for newegg-tracker"""
import argparse
import json
import os
import Tracker
import Graphic

if not os.path.exists('./Tracker/data.json'):
    with open("./Tracker/data.json", "w") as file:
        empty_data = {
            "last-updated": "",
            "number-of-items": 0,
            "items": {
            }
        }
        json.dump(empty_data, file, indent=4)

#TODO: This function is too big.
def main():
    """Command line parser"""
    parser = argparse.ArgumentParser(description='Newegg tracker application')
    parser.add_argument('Gui', metavar='Gui', type=str, help='Enter Y or N.')
    parser.add_argument('-a', '--add', type=str, help='Enter a tag to start tracking')
    parser.add_argument('-d', '--delete', type=str, help='Enter a tag to stop tracking')
    args = parser.parse_args()
    gui = args.Gui

    #Cannot update the data before I check if it's the first use
    #TODO: Maybe modify the update_data method so I can update ASAP and get_data after that stored into a variable (cleaner code)
    if not Tracker.NeweggTracker().get_data()['items']:
        if not args.add:
            print("You have no items tracked yet. Would you like to track one? Execute python main.py -h for help")
            return

    Tracker.NeweggTracker().update_data()
    data = Tracker.NeweggTracker().get_data()

    if gui == "Y":
        app = Graphic.Application(data)
    elif gui == 'N':
        if args.add:
            Tracker.NeweggTracker().add_a_new_item(args.add)
        elif args.delete:
            Tracker.NeweggTracker().remove_an_existing_item(args.delete)
        else:
            for tag, _data in data['items'].items():
                print(_data['product-name'])
                print(list(_data['history'].values())[-1]) #Gets the most recent price
                if _data['metadata']:
                    print(_data['metadata'])
                print(f"https://www.newegg.ca/{tag}")
                print("-"*150)
                print()
    else:
        print("Invalid argument. Use command -h to get help.")

if __name__ == '__main__':
    main()
