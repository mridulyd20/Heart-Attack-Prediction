import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from tkinter import messagebox
import tkinter.messagebox as msgbox
import pygame
import cv2

# Initialize pygame mixer
pygame.mixer.init()

def shaking_warning(title, message):
    warning_win = tk.Toplevel(root)
    warning_win.title(title)
    warning_win.geometry("300x100")
    warning_win.resizable(False, False)

   # Play custom beep sound 
    pygame.mixer.music.load("Siren.wav")
    pygame.mixer.music.play()

    label = tk.Label(warning_win, text=message, font=("Helvetica", 12))
    label.pack(expand=True, pady=20)

    warning_win.update_idletasks()

    # Center the window
    screen_width = warning_win.winfo_screenwidth()
    screen_height = warning_win.winfo_screenheight()
    window_width = 300
    window_height = 100
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))
    warning_win.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


    # Shake effect
    def do_shake():
        for _ in range(10):
            warning_win.geometry(f"+{center_x + 10}+{center_y}")
            warning_win.update()
            warning_win.after(50)
            warning_win.geometry(f"+{center_x - 10}+{center_y}")
            warning_win.update()
            warning_win.after(50)
        warning_win.geometry(f"+{center_x}+{center_y}")

    warning_win.after(100, do_shake)

    # Auto-close after 3 seconds
    warning_win.after(3000, warning_win.destroy)



# Function to predict heart attack
def predict_heart_attack():
    # Check if any field is empty before predicting
    for var in input_vars:
        if var.get() == "":
            shaking_warning("Incomplete Data", "Please fill all fields before predicting!")
            return  # Stop prediction if any field is empty
        
    # Get user input from entry widgets
    age = int(input_vars[0].get())
    sex = int(input_vars[1].get())
    cp = int(input_vars[2].get())
    trestbps = int(input_vars[3].get())
    chol = int(input_vars[4].get())
    fbs = int(input_vars[5].get())
    restecg = int(input_vars[6].get())
    thalach = int(input_vars[7].get())
    exang = int(input_vars[8].get())
    oldpeak = float(input_vars[9].get())
    slope = int(input_vars[10].get())
    ca = int(input_vars[11].get())
    thal = int(input_vars[12].get())

    # Create a DataFrame with user input data
    user_data = pd.DataFrame({
        'Age': [age],
        'Sex': [sex],
        'Chest Pain Type': [cp],
        'Resting Blood Pressure': [trestbps],
        'Cholesterol': [chol],
        'Fasting Blood Sugar': [fbs],
        'Resting Electrocardiographic Results': [restecg],
        'Maximum Heart Rate Achieved': [thalach],
        'Exercise Induced Angina': [exang],
        'ST Depression Induced by Exercise Relative to Rest': [oldpeak],
        'Slope': [slope],
        
        'Number of Major Vessels Colored by Fluorosopy': [ca],
        'Thalassemia': [thal]
    })

    # Use your prediction model to predict heart attack
    # Here, we are assuming a simple rule-based prediction logic as an example
    # Replace this logic with your actual prediction model
    # For example, you can use a trained machine learning model
    # to predict the probability of heart attack and apply a threshold
    # to classify the prediction as 0 or 1.


    if (age > 50 and chol > 240) or (trestbps > 140 and exang == 1) or (thalach < 120):
        prediction = 1
    else:
        prediction = 0
    
    # Display prediction
    prediction_label.config(text=f"Prediction: {prediction}")

    # Overlay image based on prediction
    if prediction == 1:
        overlay_image_path = "graph_up.png"
    else:
        overlay_image_path = "graphdownimage.jpg"
    
    overlay_image = Image.open(overlay_image_path)
    overlay_image = overlay_image.resize((300, 300), Image.LANCZOS)
    overlay_photo = ImageTk.PhotoImage(overlay_image)
    overlay_label.config(image=overlay_photo)
    overlay_label.image = overlay_photo
    overlay_label.place(x=1300, y=620, anchor="se")  # Position at bottom right

    

# Function to clear all input fields
def clear_inputs():
    for var in input_vars:
        var.set("")
     # Clear the graph image
    overlay_label.config(image="")  # Remove the image
    overlay_label.image = None  


# Function to save inputs to Excel
import os
def save_to_excel():
    # Check if any field is empty
    for var in input_vars:
        if var.get() == "":
            messagebox.showwarning("Incomplete Data", "Please fill all fields before saving!")
            return  # Stop function if any field is empty

    # Ask confirmation
    confirm = messagebox.askyesno("Confirm Save", "Are you sure you want to save the data?")
    if not confirm:
        return  # If user clicks No, cancel save
    
    # Get user input from entry widgets
    age = int(input_vars[0].get())
    sex = int(input_vars[1].get())
    cp = int(input_vars[2].get())
    trestbps = int(input_vars[3].get())
    chol = int(input_vars[4].get())
    fbs = int(input_vars[5].get())
    restecg = int(input_vars[6].get())
    thalach = int(input_vars[7].get())
    exang = int(input_vars[8].get())
    oldpeak = float(input_vars[9].get())
    slope = int(input_vars[10].get())
    ca = int(input_vars[11].get())
    thal = int(input_vars[12].get())

    # Create a DataFrame from user input data
    user_data = pd.DataFrame({
        'Age': [age],
        'Sex': [sex],
        'Chest Pain Type': [cp],
        'Resting Blood Pressure': [trestbps],
        'Cholesterol': [chol],
        'Fasting Blood Sugar': [fbs],
        'Resting Electrocardiographic Results': [restecg],
        'Maximum Heart Rate Achieved': [thalach],
        'Exercise Induced Angina': [exang],
        'ST Depression Induced by Exercise Relative to Rest': [oldpeak],
        'Slope': [slope],
        'Number of Major Vessels Colored by Fluorosopy': [ca],
        'Thalassemia': [thal]
    })
    if (age > 50 and chol > 240) or (trestbps > 140 and exang == 1) or (thalach < 120):
        prediction = 1
    else:
        prediction = 0
    # Save user input data along with prediction to Excel file
    user_data['Prediction'] = prediction
   
    # Save DataFrame to Excel file

    if os.path.exists('user_input_data.xlsx'):
        existing_data = pd.read_excel('user_input_data.xlsx')
        updated_data = pd.concat([existing_data, user_data], ignore_index=True)
        updated_data.to_excel('user_input_data.xlsx', index=False)
    else:
        user_data.to_excel('user_input_data.xlsx', index=False)

     # Show pop-up after saving
    messagebox.showinfo("Success", "Data Saved Successfully!")


# Create the main window
root = tk.Tk()
root.title("Heart Attack Prediction System")
root.geometry("1920x1080")

# Load background video
cap = cv2.VideoCapture('vid.mp4')  # Your video file

# Create a Label to display the video frames
background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def update_background():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_CUBIC) # Match window size
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        background_label.imgtk = imgtk
        background_label.config(image=imgtk)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
    background_label.after(20, update_background)

update_background()


# Create overlay label
overlay_label = tk.Label(root)
overlay_label.place(x=0, y=0)  # Initially positioned off-screen

# Create input labels and entry widgets
input_labels = ['Age:', 'Sex (Male:0,Female:1):', 'Chest Pain Type:', 'Resting Blood Pressure:', 'Cholesterol:', 
                'Fasting Blood Sugar:', 'Resting Electrocardiographic Results:', 'Maximum Heart Rate Achieved:', 
                'Exercise Induced Angina:', 'ST Depression Induced by Exercise Relative to Rest:', 'Slope:', 
                'Number of Major Vessels Colored by Fluorosopy:', 'Thalassemia:']
input_vars = [tk.StringVar() for _ in range(len(input_labels))]

for i, label_text in enumerate(input_labels):
    label = tk.Label(
        root,
        text=label_text,
        background='grey',
        font=("Arial Black",9)
    )
    label.place(x=20, y=20 + i * 50,width=360,height=30)
    entry = tk.Entry(
         root,
         textvariable=input_vars[i],
         font=("bold",18),
         background="limegreen",
         foreground="Black",
         insertbackground="Black",
         insertwidth=4

     )
   
    entry.place(x=380, y=20 + i * 50,width=150, height=30)

# Create prediction button
def on_enter_predict(e):
    predict_button.config(bg="grey", fg="black")

def on_leave_predict(e):
    predict_button.config(bg="white", fg="black")

predict_button = tk.Button(
    root,
    command=predict_heart_attack,
    text="Predict",
    bg="#ffffff",
    fg="black",
    font=("Helvetica", 14, "bold"),
    relief="groove",
    
)
predict_button.place(x=1100,y=20)

# Hover effect
predict_button.bind("<Enter>", on_enter_predict)
predict_button.bind("<Leave>", on_leave_predict)


# Create clear all button
def on_enter_clear(e):
    clear_button.config(bg="grey", fg="black")

def on_leave_clear(e):
    clear_button.config(bg="white", fg="black")

clear_button = tk.Button(
    root,
    command=clear_inputs,
    text="Clear all",
    bg="#ffffff",
    fg="black",
    font=("Helvetica", 14, "bold"),
    relief="groove",
    
)
clear_button.place(x=1100,y=80)

# Hover effect
clear_button.bind("<Enter>", on_enter_clear)
clear_button.bind("<Leave>", on_leave_clear)

# Create save to excel button
def on_enter_save(e):
    save_button.config(bg="grey", fg="black")

def on_leave_save(e):
    save_button.config(bg="white", fg="black")

save_button = tk.Button(
    root,
    command=save_to_excel,
    text="Save",
    bg="#ffffff",
    fg="black",
    font=("Helvetica", 14, "bold"),
    relief="groove",
    
)
save_button.place(x=1100,y=140)

# Hover effect
save_button.bind("<Enter>", on_enter_save)
save_button.bind("<Leave>", on_leave_save)

# Create prediction label
def on_enter(e):
    prediction_label.config(bg="grey", fg="black")

def on_leave(e):
    prediction_label.config(bg="white", fg="black")

prediction_label = tk.Label(
    root,
    text="Prediction:",
    bg="white",
    fg="black",
    font=("Helvetica", 14, "bold"),
    relief="groove",
    bd=4,
    padx=50,
    pady=5
)
prediction_label.place(x=1050,y=250)



# Run the main event loop
root.mainloop() 