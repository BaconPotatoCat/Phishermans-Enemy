import tkinter as tk
import os
from Phishermans_Enemy import *
from tkinter import font as tkfont

class mainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.text_font = tkfont.Font(family='Helvetica', size=11, weight="bold", slant="italic")
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
        button1 = tk.Button(self, text="Predict a URL", command=lambda: controller.show_frame("PredictURL"))
        button2 = tk.Button(self, text="Show Past Predictions", command=lambda: controller.show_frame("PastPredict"))
        button3 = tk.Button(self, text="Exit Program", command=lambda: quitProgram(controller))
        button1.pack()
        button2.pack()
        button3.pack()

        def quitProgram(c):
            c.destroy()

class PredictURL(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Prints out the wording title in the application
        label = tk.Label(self, text="Enter a URL to predict if its a phishing site:", font=controller.title_font)
        label1 = tk.Label(self, text="", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        label1.pack(side="top", fill="x", pady=10)
        tk.Label(self, text="URL")

        label3 = tk.Label(self, text="Model Selection:", font=controller.text_font)
        label3.pack(side="top", fill="x", pady=10)
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

        entry_user = tk.Entry(self, width=20, cursor="xterm")
        entry_user.pack()

        button3 = tk.Button(self, text='Predict', command=lambda: getpredict())
        button4 = tk.Button(self, text="Back to main", command=lambda: controller.show_frame("StartPage"))
        button3.pack()
        button4.pack()

        # Place in the code for predict function
        def getpredict():
            entry1 = entry_user.get()
            model = int(val.get())
            rerunChoice = int(rerun.get())
            if checkPrediction(entry1, model) or rerunChoice == 1:
                predictStatus = runPredict(entry1,model)
            else:
                # Only if predict function return a value
                if rerunChoice == 2:
                    label1.config(text="Completed. Please view the results in the 'Past Predictions' page.")
                else:
                    label1.config(text="An error has occured and the prediction was not complete.")

class PastPredict(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Past Predictions", font=controller.title_font)
        label1 = tk.Label(self, text="", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        label1.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text='Load Server', command=lambda: loadServer())
        button2 = tk.Button(self, text="Back to main", command=lambda: controller.show_frame("StartPage"))
        button1.pack()
        button2.pack()
        # Place in the code for predict function
        def loadServer():
            os.system("start cmd /k python Flask_Report.py")
            button1.config(state="disabled")
            label1.config(text="Go to localhost:5000 to view the report. Close the command prompt to stop the server.")

if __name__ == "__main__":
    app = mainApp()
    app.title("Phisherman's Enemy")
    app.mainloop()