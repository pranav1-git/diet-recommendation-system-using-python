import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd


def get_output():
    # Retrieve user inputs from the GUI
    user_age = age_entry.get()
    user_height = height_entry.get()
    user_weight = weight_entry.get()
    user_bmi_text = bmi_label.cget("text")
    user_diet_type = diet_type.get()  # "All", "Veg", or "Non-Veg"
    user_diet_preference = diet_type_preference.get()  # "High-Protein", "Keto", "None"
    user_health_condition = (
        diet_type_health_conditions.get()
    )  # "None", "Diabetes", etc.
    user_diet_goal = (
        selected_goal if selected_goal else "None"
    )  # "Weight Loss", "Muscle Gain", "Healthy"

    # Validate user input
    if not (user_age and user_height and user_weight and user_bmi_text):
        messagebox.showwarning("Input Error", "Please fill in all the required fields!")
        return
    if int(user_age) > 80 or int(user_age) < 5:
        messagebox.showwarning("Age Value Error", "Please provide age between 5 and 80")
        return
    if int(user_height) > 300 or int(user_height) < 60:
        messagebox.showwarning(
            "Height Value Error", "Please provide height ( in cm ) between 60 and 300"
        )
        return

    if int(user_weight) > 500 or int(user_weight) < 30:
        messagebox.showwarning("Age Value Error", "Please provide age between 5 and 80")
        return
    try:
        user_bmi = float(user_bmi_text)
        user_weight = float(user_weight)
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid numerical values entered!")
        return

    # Load food data
    try:
        df = pd.read_csv("food_data.csv")
    except Exception as e:
        messagebox.showerror("File Error", f"Error reading food_data.csv: {e}")
        return

    # Filtering function
    def contains_value(cell_value, target):
        if pd.isna(cell_value):
            return False
        return target.lower() in str(cell_value).lower().split(", ")

    # Filter based on Diet Type
    if user_diet_type != "All":
        df = df[df["Category"].str.lower() == user_diet_type.lower()]

    # Filter based on Health Condition
    if user_health_condition == "High cholesterol":
        df = df[(df["Fats"] < 15) & (df["Fibre"] > 2) & (df["Sugar"] < 5)]
    elif user_health_condition == "Diabetes":
        df = df[(df["Sugar"] < 5) & (df["Fibre"] > 4)]
    elif user_health_condition == "Hypertension":
        df = df[df["Sodium"] < 400]  # Assuming Sodium column exists
    elif user_health_condition == "Iron Deficiency":
        df = df[df["Iron"] > 2]

    # Filter based on Diet Goal
    if user_diet_goal == "Weight Loss":
        df = df[(df["Calories"] <= 300)]
        # Filter based on Diet Preferences
        if user_diet_preference == "High-Protein":
            df = df.sort_values(
                "Protein", ascending=False
            )  # Prioritize high-protein foods
        elif user_diet_preference == "Keto":
            df = df.sort_values(
                "Carbohydrates", ascending=True
            )  # Prioritize low-carb foods
            df = df.sort_values("Fats", ascending=False)  # High-fat for keto

        # df = df.sort_values(["Fibre", "Protein"], ascending=[False, False])

    elif user_diet_goal == "Muscle Gain":
        df = df[df["Calories"] >= 300]

        # Filter based on Diet Preferences
        if user_diet_preference == "High-Protein":
            df = df.sort_values(
                "Protein", ascending=False
            )  # Prioritize high-protein foods
        elif user_diet_preference == "Keto":
            df = df.sort_values(
                "Carbohydrates", ascending=True
            )  # Prioritize low-carb foods
            df = df.sort_values("Fats", ascending=False)  # High-fat for keto

        # df = df.sort_values(["Protein", "Fats"], ascending=[False, False])

        # if user_bmi < 18.5:  # Underweight: prioritize higher calories
        #         df_meal = df_meal[df_meal["Calories"] > 500]
    elif user_diet_goal == "Healthy":
        df = df[(df["Calories"] > 100) & (df["Calories"] < 300)]
        # Filter based on Diet Preferences
        if user_diet_preference == "High-Protein":
            df = df.sort_values(
                "Protein", ascending=False
            )  # Prioritize high-protein foods
        elif user_diet_preference == "Keto":
            df = df.sort_values(
                "Carbohydrates", ascending=True
            )  # Prioritize low-carb foods
            df = df.sort_values("Fats", ascending=False)  # High-fat for keto

        # df = df.sort_values(["Fibre", "Protein"], ascending=[False, False])

    # Create meal plan dictionary
    meal_plan = {"breakfast": [], "lunch": [], "snack": [], "dinner": []}

    for meal in meal_plan.keys():
        df_meal = df[df["Meal Type"].apply(lambda x: contains_value(x, meal))]
        meal_plan[meal] = df_meal["Food_items"].head(4).tolist()

    def show_output_popup():
        output_window = tk.Toplevel(root, bg=app_bg)
        output_window.title("Meal Plan Recommendation")
        top_level_width = 1300
        top_level_height = 590
        output_window.geometry(f"{top_level_width}x{top_level_height}")
        title_label = tk.Label(
            output_window,
            text="DIETIFY",
            font=(app_font_family, 32, "bold"),
            bg=app_bg,
            fg="white",
            border=0,
        )
        title_label.place(x=x_value, y=33)
        project_name_label = tk.Label(
            output_window,
            text="PERSONALIZED DIET RECOMMENDATION SYSTEM",
            font=(app_font_family, app_font_size),
            bg=app_text_bg,
            pady=7,
            padx=15,
            border=0,
        )
        project_name_label.place(x=x_value, y=95)
        breakfast_label = tk.Label(
            output_window,
            text="Breakfast",
            font=(app_font_family, 18),
            bg=app_bg,
            fg="white",
            border=0,
        )
        breakfast_label.place(x=x_value, y=180)
        breakfast_label = tk.Label(
            output_window,
            text="Breakfast",
            font=(app_font_family, 19),
            bg=app_bg,
            fg="white",
            border=0,
        )
        breakfast_label.place(x=x_value, y=180)
        frame_inside_ow = tk.Frame(
            output_window,
            bg=app_text_bg,
            border=0,
            pady=10,
        )
        frame_inside_ow.place(x=x_value, y=230, height=250)
        for meal in meal_plan["breakfast"]:
            each_meal_label = tk.Label(
                frame_inside_ow,
                text=meal.capitalize(),
                font=(app_bg, 14),
                bg=app_text_bg,
                fg="#2b3b0f",
                border=0,
                padx=5,  # Adjust padding
                pady=5,  # Adjust padding
            )
            each_meal_label.pack(anchor="w", padx=15)  # Align text to the left
            # /////////
        lunch_label = tk.Label(
            output_window,
            text="Lunch",
            font=(app_font_family, 19),
            bg=app_bg,
            fg="white",
            border=0,
        )
        lunch_label.place(x=340, y=180)
        frame_inside_ow = tk.Frame(
            output_window,
            bg=app_text_bg,
            border=0,
            pady=10,
        )
        frame_inside_ow.place(x=340, y=230, height=250)
        for meal in meal_plan["lunch"]:
            each_meal_label = tk.Label(
                frame_inside_ow,
                text=meal.capitalize(),
                font=(app_bg, 14),
                bg=app_text_bg,
                fg="#2b3b0f",
                border=0,
                padx=5,  # Adjust padding
                pady=5,  # Adjust padding
            )
            each_meal_label.pack(anchor="w", padx=15)
        # /////////
        snack_label = tk.Label(
            output_window,
            text="Snack",
            font=(app_font_family, 19),
            bg=app_bg,
            fg="white",
            border=0,
        )
        snack_label.place(x=620, y=180)
        frame_inside_ow = tk.Frame(
            output_window,
            bg=app_text_bg,
            border=0,
            pady=10,
        )
        frame_inside_ow.place(x=620, y=230, height=250)
        for meal in meal_plan["snack"]:
            each_meal_label = tk.Label(
                frame_inside_ow,
                text=meal.capitalize(),
                font=(app_bg, 14),
                bg=app_text_bg,
                fg="#2b3b0f",
                border=0,
                padx=5,  # Adjust padding
                pady=5,  # Adjust padding
            )
            each_meal_label.pack(anchor="w", padx=15)
        # ///////////////
        dinner_label = tk.Label(
            output_window,
            text="Dinner",
            font=(app_font_family, 19),
            bg=app_bg,
            fg="white",
            border=0,
        )
        dinner_label.place(x=900, y=180)
        frame_inside_ow = tk.Frame(
            output_window,
            bg=app_text_bg,
            border=0,
            pady=10,
        )
        frame_inside_ow.place(x=900, y=230, height=250)
        for meal in meal_plan["dinner"]:
            each_meal_label = tk.Label(
                frame_inside_ow,
                text=meal.capitalize(),
                font=(app_bg, 14),
                bg=app_text_bg,
                fg="#2b3b0f",
                border=0,
                padx=5,  # Adjust padding
                pady=5,  # Adjust padding
            )
            each_meal_label.pack(anchor="w", padx=15)

    show_output_popup()


# function that opens app at the center
def center_window(window, width, height):
    """
    Center the Tkinter window on the screen.
    :param window: The Tkinter window or root object.
    :param width: Width of the window.
    :param height: Height of the window.
    """
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y positions to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the window's geometry
    window.geometry(f"{width}x{height}+{x}+{y-30}")


# def exit_app():
#     root.destroy()


def select_goal(goal):
    global selected_goal
    selected_goal = goal
    for button in goal_buttons:
        if button[0] == goal:
            button[1].config(bg="#00ffdd", fg="black")  # Highlight selected button
        else:
            button[1].config(bg="#ddf2c4", fg="black")  # Reset other buttons


# calculating the bmi
def calculate_bmi():

    try:
        height = float(height_entry.get()) / 100  # Convert cm to meters
        weight = float(weight_entry.get())
        bmi = weight / (height**2)
        bmi_label.config(text=f"{bmi:.2f}")
    except ValueError:
        bmi_label.config(text="")


root = tk.Tk()
root.title("Personalized Diet Recommendation System")
# print(font.families())
# Set the window size
window_width = 870
window_height = 690
root.geometry(f"{window_width}x{window_height}")
app_bg = "#457044"
app_text_bg = "#e9ffcf"
app_font_size = 14
app_label_fsize = 12
app_font_family = "Arial"
root.configure(bg=app_bg)

padx_value = 30
pady_value = 3
x_value = 60


# Center the window
center_window(root, window_width, window_height)


# setting an image to background
def resize_bg(event):
    """Resize the background image to fit the window."""
    global bg_img, bg_photo  # Keep references to avoid garbage collection

    # Resize image to match new window size
    bg_img = external_img.resize((event.width, event.height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    # Update label background
    bg_label.config(image=bg_photo)
    bg_label.image = bg_photo


external_img = Image.open("diet-bg-image.jpg")  # Replace with your image
bg_photo = ImageTk.PhotoImage(external_img)
bg_label = tk.Label(root, image=bg_photo, border=0)
# bg_label.place(x=350, y=170, relwidth=0.6, relheight=0.6)
bg_label.place(x=480, y=370, relwidth=0.5, relheight=0.5)
root.bind("<Configure>", resize_bg)


# validating the user input
# def validate_input(new_value, field):
#     """Validate user input based on the given field type."""
#     if new_value == "":  # Allow empty field (for deletion)
#         return True
#     try:
#         value = float(new_value)
#         if field == "age" and (0 <= value <= 100):
#             return True
#         elif field in ["height"] and (0 <= value <= 500):
#             return True
#         elif field in ["weight"] and (0 <= value <= 500):
#             return True
#     except ValueError:
#         return False  # Reject non-numeric input

#     return False  # Reject values outside the range


# validate_age = root.register(lambda new_value: validate_input(new_value, "age"))
# validate_height = root.register(lambda new_value: validate_input(new_value, "height"))
# validate_weight = root.register(lambda new_value: validate_input(new_value, "weight"))


# GUI ka starting
title_label = tk.Label(
    root,
    text="DIETIFY",
    font=(app_font_family, 32, "bold"),
    bg=app_bg,
    fg="white",
    border=0,
)
title_label.place(x=x_value, y=33)
project_name_label = tk.Label(
    root,
    text="PERSONALIZED DIET RECOMMENDATION SYSTEM",
    font=(app_font_family, app_font_size),
    bg=app_text_bg,
    pady=7,
    padx=15,
    border=0,
)
project_name_label.place(x=x_value, y=95)


# Age Field
age_label = tk.Label(
    root,
    text="AGE",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
age_label.place(x=x_value, y=170)
age_entry = tk.Entry(
    root,
    font=(app_font_family, app_font_size),
    bg="white",
    validate="key",
    # validatecommand=(validate_age, "%P"),
    border=0,
)
age_entry.place(x=x_value, y=203)


# managing diet type
diet_type_label = tk.Label(
    root,
    text="DIET TYPE",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
diet_type_label.place(x=330, y=170)
diet_type = ttk.Combobox(
    root,
    values=["All", "Veg", "Non-Veg"],
    state="readonly",
    font=(app_font_family, app_font_size),
)
diet_type.place(x=330, y=200)
diet_type.current(0)


# Height Field
height_label = tk.Label(
    root,
    text="HEIGHT IN CM",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
height_label.place(x=x_value, y=250)
height_entry = tk.Entry(
    root,
    font=(app_font_family, app_font_size),
    validate="key",
    # validatecommand=(validate_height, "%P"),
    border=0,
)
height_entry.place(x=x_value, y=280)


# managing diet perferences
diet_preferences = tk.Label(
    root,
    text="DIET PREFERENCES",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
diet_preferences.place(x=330, y=250)
diet_type_preference = ttk.Combobox(
    root,
    values=["None", "High-Protein", "Keto"],
    state="readonly",
    font=(app_font_family, app_font_size),
)
diet_type_preference.place(x=330, y=280)
diet_type_preference.current(0)


# Weight Field
weight_label = tk.Label(
    root,
    text="WEIGHT IN KG",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
weight_label.place(x=x_value, y=330)
weight_entry = tk.Entry(
    root,
    font=(app_font_family, app_font_size),
    validate="key",
    # validatecommand=(validate_weight, "%P"),
    border=0,
)
weight_entry.place(x=x_value, y=363)


# managing user health conditions
health_condiiton = tk.Label(
    root,
    text="HEALTH CONDITIONS",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
health_condiiton.place(x=330, y=330)
diet_type_health_conditions = ttk.Combobox(
    root,
    values=[
        "None",
        "High cholesterol",
        "Diabetes",
        "Hypertension",
        "Iron Deficiency",
    ],
    state="readonly",
    font=(app_font_family, app_font_size),
)
diet_type_health_conditions.place(x=330, y=363)
diet_type_health_conditions.current(0)


# Bind KeyRelease events to calculate BMI
height_entry.bind("<KeyRelease>", lambda event: calculate_bmi())
weight_entry.bind("<KeyRelease>", lambda event: calculate_bmi())


# managing bmi
bmi_text_label = tk.Label(
    root,
    text="BMI",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
bmi_text_label.place(x=x_value, y=410)
bmi_label = tk.Label(
    root,
    text="BMI : ",
    font=(app_font_family, app_font_size),
    bg="white",
    width=19,
    anchor="w",
    padx=5,
    pady=1,
    border=0,
)
bmi_label.place(x=x_value, y=440)


# managing goal
selected_goal = None
goal_label = tk.Label(
    root,
    text="FITNESS GOAL",
    font=(app_font_family, app_label_fsize),
    bg=app_bg,
    fg="white",
    border=0,
)
goal_label.place(x=x_value, y=490)
goals = ["Weight Loss", "Muscle Gain", "Healthy"]


goal_buttons = []
frame = tk.Frame(root, bg=app_bg, border=0)
frame.place(x=x_value, y=520)

for goal in goals:
    btn = tk.Button(
        frame,
        text=goal,
        font=(app_font_family, app_font_size),
        width=13,
        bg=app_text_bg,
        command=lambda g=goal: select_goal(g),
        border=0,
    )
    # btn.place(x=x_value, y=520)
    if goal == "Weight Loss":
        btn.pack(side="left", padx=(0, 10))
    elif goal == "Healthy":
        btn.pack(side="left", padx=(10, 0))
    else:
        btn.pack(side="left", padx=10)
    goal_buttons.append((goal, btn))


# exit_button = tk.Button(
#     root,
#     text="Exit",
#     font=(app_font_family, app_font_size, "bold"),
#     bg="red",
# command=exit_app,
#     border=0,
#     width=8,
# )
# exit_button.place(x=x_value, y=550)


def get_user_inputs():
    try:
        user_age = age_entry.get()
        user_height = height_entry.get()
        user_weight = weight_entry.get()
        user_bmi = bmi_label.cget("text")  # Get displayed BMI text
        user_diet_type = diet_type.get()
        user_diet__type_preference = diet_type_preference.get()
        user_health_condition = diet_type_health_conditions.get()
        user_diet_goal = selected_goal if selected_goal else "None"

        print("User Inputs:")
        print("Age:", user_age)
        print("Height:", user_height)
        print("Weight:", user_weight)
        print("BMI:", user_bmi)
        print("Diet Type:", user_diet_type)
        print("Fitness Goal:", user_diet_goal)
        print("Diet Preferences:", user_diet__type_preference)
        print("Health Conditions:", user_health_condition)
    except Exception as e:
        print("Error retrieving user inputs:", e)


# Add a button to test retrieving inputs
test_button = tk.Button(
    root,
    font=(app_font_family, app_label_fsize),
    bg=app_text_bg,
    text="OUTPUT",
    command=get_output,
    width=16,
    pady=3,
    border=0,
)
test_button.place(x=x_value, y=590)


root.mainloop()
