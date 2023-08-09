'''
Author: Arthur Zussman
Date: [Current Date]
Description: [A task manager app that allows users to add, update, and track their tasks]
'''

# Importing relevant libraries
from datetime import date
from datetime import datetime
import uuid
import os
from PIL import Image
import shutil
import csv


class Task:
    def __init__(self, identifier, title, description, due_date, status="Pending"):
        # Initialize task attributes
        self.identifier = identifier
        self.title = title
        self.description = description
        self.due_date = due_date or date.today().date() #Set current date if due_date is not provided
        self.status = status


class TaskManager:
    def __init__(self):
        # Initialize an empty list to store tasks
        self.tasks = []
        
    def add_task(self):
        # Add a new task to the list
        identifier = str(uuid.uuid4()) # Generate a Universally Unique Identifier as the identifier
        title = str(input("Enter task title:"))
        description = str(input("Enter task description:"))
        due_date = str(input("Enter task due date (DD/MM/YYYY):"))
        image_path = str(input("Enter image path (leave blank if no image):"))
        
        # Validate due_date format
        try:
            due_date = datetime.strptime(due_date, "%d/%m/%Y").date()
        except ValueError:
            print("Invalid due date format. Please use DD/MM/YYYY format.")
            return
        
        # Validate due_date is no in the past
        if due_date < datetime.today().date():
            print("Due date cannot be in the past.")
            return
        
        if image_path:
            image_filename = f"{identifier}.jpg" # Generate a unique file name for the image
            destination = os.path.join("Taskenator", "uploadedimages", image_filename)
            os.makedirs(os.path.dirname(destination), exist_ok=True) # Create the "uploadedimages" directory if it doesn't exist
            
            # Check the image format
            try:
                # Open the image for processing
                with Image.open(image_path) as image:
                
                    valid_formats = ["JPEG", "PNG", "GIF"]
                
                    if image.format in valid_formats:
                        shutil.move(image_path, destination)
                    else:
                        print("Invalid image format. Only JPEG, PNG, and GIF formats are supported.")
                    
            except Exception as e:
                print(f"Error processing image:{e}")
        
        task = Task(identifier, title, description, due_date)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task ID: {task.identifier}, Title: {task.title}, Description: {task.description}, Due Date: {task.due_date}, Status: {task.status}")
    
    def save_tasks(self):
        filename = "tasks.csv"
        directory = os.path.join("Taskenator", "tasks_saved")
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        
        with open(filepath, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['ID', 'Title', 'Description', 'Due Date', 'Status'])
                
            new_task = self.tasks[-1] # Obtain only the last task added    
                
            # for task in self.tasks:
            writer.writerow([new_task.identifier, new_task.title, new_task.description, new_task.due_date, new_task.status])
        
    def update_task(self, 
                    task_id, 
                    new_title=None, 
                    new_description=None,
                    new_due_date=None, 
                    new_status=None):
        # Update an existing task with new information
        task = self.get_task_by_id(task_id)
        if task:
            # Check if each attribute is provided and update accordingly
            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            if new_due_date:
                task.due_date = new_due_date
            if new_status:
                task.status = new_status
            return True  
        return False
    
    def mark_task_as_complete(self, task_id):
        return self.update_task(task_id, new_status='Completed')
    
    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def delete_tasks_file(self):
        filename = "tasks.csv"
        directory = os.path.join("Taskenator", "tasks_saved")
        filepath = os.path.join(directory, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            print("File 'tasks.csv' deleted successfully.")
        else:
            print("File 'tasks.csv' does not exist.")
    
    def get_task_by_id(self, task_id):
        # Retrieve a task from the list based on its ID
        tasks_with_id = [task for task in self.tasks if task.identifier == task_id]
        if tasks_with_id:
            return tasks_with_id[0]
        return None
    
    
# Example usage
task_manager = TaskManager()
task_manager.add_task() # esse comando será atribuido a um botão na GUI

if task_manager.tasks:
    # Print the added task
    task = task_manager.tasks[0]
else:
    print("Failed to add task.")    
