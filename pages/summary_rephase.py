import customtkinter
from DatabaseHandler import DatabaseHandler
from components.MessageBox import show_thanks, show_error
from tkinter import filedialog
import nltk
from nltk.tokenize import sent_tokenize
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.corpus import wordnet
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    words = nltk.word_tokenize(text)
    return [word.lower() for word in words if word.lower() not in stop_words]

def sentence_similarity(sent1, sent2):
    vector1 = [word.lower() for word in sent1]
    vector2 = [word.lower() for word in sent2]
    all_words = list(set(vector1 + vector2))

    vector1_count = [0] * len(all_words)
    vector2_count = [0] * len(all_words)

    for w in vector1:
        if w in all_words:
            vector1_count[all_words.index(w)] += 1

    for w in vector2:
        if w in all_words:
            vector2_count[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1_count, vector2_count)

def build_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j])

    return similarity_matrix

def generate_summary_from_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    sentence_similarity_matrix = build_similarity_matrix(sentences)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    summary = []
    for i in range(num_sentences):
        summary.append(ranked_sentences[i][1])

    return "\n".join(summary)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
def rephrase_sentence(text):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    rephrased_sentence = []

    for word, tag in tagged:
        if tag.startswith('NN'):  # Nouns
            synsets = wordnet.synsets(word, pos=wordnet.NOUN)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        elif tag.startswith('VB'):  # Verbs
            synsets = wordnet.synsets(word, pos=wordnet.VERB)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        elif tag.startswith('JJ'):  # Adjectives
            synsets = wordnet.synsets(word, pos=wordnet.ADJ)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        elif tag.startswith('RB'):  # Adverbs
            synsets = wordnet.synsets(word, pos=wordnet.ADV)
            if synsets:
                rephrased_sentence.append(synsets[0].lemmas()[0].name())
            else:
                rephrased_sentence.append(word)
        else:
            rephrased_sentence.append(word)

    return ' '.join(rephrased_sentence)








def SummaryTab(self, parentSecondFrame):
    tabview_2 = customtkinter.CTkTabview(parentSecondFrame, width=900)
    tabview_2.pack(pady=10, padx=10)
    searchTab = tabview_2.add("Summary")
    updateTab = tabview_2.add("Rephrase")
    

    # ?############################################################################################
    # ? Search Transaction Tab
    # ?############################################################################################
    def UploadFile():
        file_path = filedialog.askopenfilename()
        if file_path:
            encodings = ['utf-8', 'latin-1']  # Add more encodings if needed
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        text = file.read()
                    print("File Contents:")
                    print(text)
                    summary = generate_summary_from_text(text)
                    summaryLabel.configure(text=summary)
                    break  # Break loop if successful
                except UnicodeDecodeError:
                    continue
    def RephraseText(self):
        # Get the text from the entry field
        original_text = self.RephraseEntry.get()

        # Rephrase the text using your rephrasing algorithm or library
        rephrased_text = rephrase_function(original_text)  # Implement this function

        # Update the GUI to display the rephrased text
        self.RephrasedText.configure(text=rephrased_text)

    self.SearchTabLabel = customtkinter.CTkLabel(
        searchTab,
        text="Summary",
        compound="center",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    ).grid(row=0, column=0, padx=50, pady=25)

    # Button to upload file
    self.UploadFileButton = customtkinter.CTkButton(
        searchTab, text="Upload File", command=UploadFile,fg_color="teal"
    ).grid(row=1, column=0, padx=10, pady=10)

    summaryLabel = customtkinter.CTkLabel(
        searchTab,
        text="Summary will appear here",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=16),
        height=5,
        wraplength=800
    )
    summaryLabel.grid(row=2, column=0, padx=20, pady=5)

    # Box where summary will be shown
    # self.SummaryBox = customtkinter.CTkLabel(
    #     summaryTab,
    #     width=80,
    #     height=20,
    #     font=customtkinter.CTkFont("Times new roman", size=12),
    # )
    # self.SummaryBox.grid(row=1, column=0, padx=10, pady=10)

    

    # ?############################################################################################
    # ? Rephrase Transaction Tab
    # ?############################################################################################
    def RephraseText():
        # Get the text from the entry field
        original_text = RephraseEntry.get()

        # Rephrase the text using your rephrasing algorithm
        rephrased_text = rephrase_sentence(original_text)

        # Update the GUI to display the rephrased text
        RephrasedText.configure(text=rephrased_text)

    self.RephraseTextLabel = customtkinter.CTkLabel(
        updateTab,
        text="Enter Text to Rephrase:",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    )
    self.RephraseTextLabel.grid(row=0, column=0, padx=50, pady=25)

    RephraseEntry = customtkinter.CTkEntry(
        updateTab,
        placeholder_text="Enter your text here...",
        font=customtkinter.CTkFont("Times new roman", size=18),
    )
    RephraseEntry.grid(row=1, column=0, padx=50, pady=10)

    RephraseButton = customtkinter.CTkButton(
        updateTab,
        text="Rephrase",
        command=RephraseText,
        fg_color="teal"
    )
    RephraseButton.grid(row=2, column=0, padx=50, pady=10)

    self.RephrasedTextLabel = customtkinter.CTkLabel(
        updateTab,
        text="Rephrased Text:",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    )
    self.RephrasedTextLabel.grid(row=3, column=0, padx=50, pady=10)

    RephrasedText = customtkinter.CTkLabel(
        updateTab,
        text="",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=16),
        wraplength=800 
    )
    RephrasedText.grid(row=4, column=0, padx=50, pady=10)

    
    