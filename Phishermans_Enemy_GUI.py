import tkinter as tk
import os
from Phishermans_Enemy import *
from tkinter import font as tkfont
from tkinter import filedialog as fd


class mainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.text_font = tkfont.Font(family='Helvetica', size=9, weight="bold")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PredictURL, PastPredict):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Phisherman's Enemy", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label1 = tk.Label(self, text="Prediction of URL", font=controller.text_font)
        label1.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Predict a URL", activebackground='#345', activeforeground='white',
                            command=lambda: controller.show_frame("PredictURL"))
        button1.pack(side=tk.TOP, ipadx=5, padx=5, pady=5)

        label2 = tk.Label(self, text="Start a flask server to view the previous predictions", font=controller.text_font)
        label2.pack(side="top", fill="x", pady=10)
        button2 = tk.Button(self, text="Show Past Predictions", activebackground='#345', activeforeground='white',
                            command=lambda: controller.show_frame("PastPredict"))
        button2.pack(side=tk.TOP, ipadx=5, padx=5, pady=5)

        label3 = tk.Label(self, text="To quit the program", font=controller.text_font)
        label3.pack(side="top", fill="x", pady=10)
        button3 = tk.Button(self, text="Exit Program", activebackground='#345', activeforeground='white',
                            command=lambda: quitProgram(controller))
        button3.pack(side=tk.TOP, ipadx=5, padx=5, pady=5)

        def quitProgram(c):
            c.destroy()


class PredictURL(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Prints out the wording title in the application
        label = tk.Label(self, text="Prediction of URL", font=controller.title_font)
        label1 = tk.Label(self, text="", font=controller.text_font)
        label.pack(side="top", fill="x")
        label1.pack(side="top", fill="x", pady=3)
        tk.Label(self, text="URL")

        label3 = tk.Label(self, text="Model Selection:", font=controller.text_font)
        label3.pack(side="top", fill="x", pady=10, padx=10)
        # Creates a variable val to store the radio btn value 1/2/3 which user selects
        val = tk.StringVar(self, 1)

        models = {"Gradient Boosting Classifier": 1,
                  "XGB Classifier": 2,
                  "Random Forest Classifier": 3}

        # Loops through the dictionary and create the radio buttons
        for (text, value) in models.items():
            tk.Radiobutton(self, text=text, variable=val, value=value).pack(side=tk.TOP, ipady=10)
        label4 = tk.Label(self, text="Rerun if prediction exists?", font=controller.text_font)
        label4.pack(side="top", fill="x", pady=10)
        # Rerun predict
        rerun = tk.StringVar(self, 1)
        values = {"Re-run prediction": 1,
                  "Cancel prediction": 2}
        # Loops through the dictionary and create the radio buttons
        for (text, value) in values.items():
            tk.Radiobutton(self, text=text, variable=rerun, value=value).pack(side=tk.TOP, ipady=10)

        label4 = tk.Label(self, text="Enter URL:", font=controller.text_font)
        label4.pack(side="top", fill="x", pady=10)

        entry_user = tk.Entry(self, width=40, cursor="xterm")
        entry_user.pack()

        button3 = tk.Button(self, text='Predict', activebackground='#345', activeforeground='white',
                            command=lambda: getpredict())
        button4 = tk.Button(self, text="Main Menu", activebackground='#345', activeforeground='white',
                            command=lambda: controller.show_frame("StartPage"))
        button4.pack(side=tk.RIGHT, ipadx=5, padx=9, pady=10)
        button3.pack(side=tk.RIGHT, ipadx=5, padx=5, pady=10)

        # Place in the code for predict function
        def getpredict():
            entry1 = entry_user.get().strip()
            model = int(val.get())
            rerunChoice = int(rerun.get())
            if entry1 == "":
                label1.config(text="Please enter a URL")
            elif checkPrediction(entry1, model) or rerunChoice == 1:
                label1.config(text="Predicting....")
                runPredict(entry1, model)
                label1.config(text="Completed. Please view the results in the 'Past Predictions' page.")
            else:
                # Only if predict function return a value
                if rerunChoice == 2:
                    label1.config(text="Prediction exists, please view the results in the 'Past Predictions' page.")
                else:
                    label1.config(text="An error has occured and the prediction was not completed.")


class PastPredict(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Past Predictions", font=controller.text_font)
        label1 = tk.Label(self, text="", font=controller.text_font)
        label.pack(side="top", fill="x", pady=10)
        label1.pack(side="top", fill="x", pady=10)
        label2 = tk.Label(self, text="Click here to load the flask server", font=controller.text_font)
        label2.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text='Load Server', activebackground='#345', activeforeground='white',
                            command=lambda: loadServer())
        button1.pack(side=tk.TOP, ipadx=5, padx=5, pady=5)
        label3 = tk.Label(self, text="Back to main", font=controller.text_font)
        label3.pack(side="top", fill="x", pady=10)
        button2 = tk.Button(self, text="Main Menu", activebackground='#345', activeforeground='white',
                            command=lambda: controller.show_frame("StartPage"))
        button2.pack(side=tk.TOP, ipadx=5, padx=5, pady=5)

        # Place in the code for predict function
        def loadServer():
            try:
                with open('Past_Predictions.csv') as f:
                    os.system("start cmd /k python Flask_Report.py")
                    button1.config(state="disabled")
                    label1.config(
                        text="Go to localhost:5000 to view the report. Close the command prompt to stop the server.")
            except FileNotFoundError:
                label1.config(text="There are no existing predictions.")


if __name__ == "__main__":
    app = mainApp()
    app.title("Phisherman's Enemy")
    app.geometry("720x550")
    app.mainloop()