import pandas as pd
import tkinter as tk


class Chatbot:
    def __init__(self, excel_file):
        # Load the Excel file
        self.df = pd.read_excel(excel_file)
        self.questions = self.df['Question'].tolist()
        self.answers = self.df['Answer'].tolist()
        self.additional_info = self.df['Additional Information'].tolist()

        # Predefined responses
        self.predefined_responses = {
            'hi': 'Hello! How can I assist you today?',
            'hello': 'Hi there! How can I help you?',
            'bye': 'Goodbye! Have a great day!',
            'okay': 'Got it! If you have any more questions, feel free to ask.'
        }

    def get_response(self, user_input):
        # Check for predefined responses
        for key in self.predefined_responses:
            if key in user_input.lower():
                return self.predefined_responses[key]

        # Check for a matching question in the Excel
        for question, answer, info in zip(self.questions, self.answers, self.additional_info):
            if user_input.lower() in question.lower():
                return f"{answer}\n\nAdditional Information: {info}"

        return "Sorry, I don't have an answer for that."


class ChatbotGUI:
    def __init__(self, chatbot):
        self.chatbot = chatbot
        self.root = tk.Tk()
        self.root.title("Nutritional Guidance Chatbot")

        # Full screen mode
        self.root.attributes('-fullscreen', True)

        # Set background color
        self.root.configure(bg='#212121')

        # Create a frame for the heading
        self.heading_frame = tk.Frame(self.root, bg='#212121')
        self.heading_frame.pack(fill=tk.X, pady=10)

        # Heading label
        self.heading_label = tk.Label(self.heading_frame, text="Nutritional Guidance Chatbot",
                                      font=('Helvetica', 20, 'bold'), bg='#212121', fg='white')
        self.heading_label.pack()

        # Create a frame for chat and history
        self.main_frame = tk.Frame(self.root, bg='#212121')
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Chat history section
        self.history_frame = tk.Frame(self.main_frame, bg='#212121')
        self.history_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Text area for chat history
        self.history_area = tk.Text(self.history_frame, width=30, bg='#333333', fg='white', wrap=tk.WORD,
                                    state=tk.DISABLED)
        self.history_area.pack(expand=True, fill=tk.Y)

        # Create a frame for the chat area
        self.chat_frame = tk.Frame(self.main_frame, bg='#212121')
        self.chat_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Text area for chat history (new messages)
        self.text_area = tk.Text(self.chat_frame, height=15, width=50, wrap=tk.WORD, bg='#333333', fg='white',
                                 insertbackground='white')
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Entry widget for user input
        self.entry_frame = tk.Frame(self.root, bg='#212121')
        self.entry_frame.pack(fill=tk.X, padx=10, pady=10)

        # Increased width for entry widget
        self.entry = tk.Entry(self.entry_frame, width=80, bg='#333333', fg='white')
        self.entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg='#444444', fg='white')
        self.send_button.pack(side=tk.RIGHT)

        # Bind ESC key to exit full screen
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.root.mainloop()

    def send_message(self, event=None):
        # Get user input and response
        user_input = self.entry.get()
        response = self.chatbot.get_response(user_input)

        # Update chat history
        self.history_area.configure(state=tk.NORMAL)
        self.history_area.insert(tk.END, f"You: {user_input}\n")
        self.history_area.configure(state=tk.DISABLED)

        # Display user input and bot response in the text area
        self.text_area.insert(tk.END, f"You: {user_input}\n")
        self.text_area.insert(tk.END, f"Bot: {response}\n\n")

        # Clear the entry widget
        self.entry.delete(0, tk.END)

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)


if __name__ == "__main__":
    # Provide the path to your Excel file
    chatbot = Chatbot('data.xlsx')
    gui = ChatbotGUI(chatbot)
