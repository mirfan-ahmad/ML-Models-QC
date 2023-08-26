import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

class Evaluate:
    def __init__(self, true_labels, true_attribute, predicted_labels, predicted_attribute, matrix_name):
        self.true_labels = true_labels
        self.true_attribute = list(true_attribute)
        self.predicted_attribute = predicted_attribute
        self.predicted_labels = list(predicted_labels)
        self.name = matrix_name
        self.storage_path = os.getcwd()
        os.mkdir('QA-Report', exist_ok=True)
        os.mkdir('Confusion-Metrices', exist_ok=True)
        self.__evaluate()


    def __evaluate(self):
        actual = pd.read_csv(self.true_labels)
        predicted = pd.read_csv(self.predicted_labels)

        # Slice the Dataframe to get the desired columns
        
        Actual_values = []
        for true in self.true_attribute:
            Actual_values.append(actual.iloc[:, true].to_list())
            
        Predicted_values = []
        for pred in self.predicted_attribute:
            Predicted_values.append(predicted.iloc[:, pred].to_list())

        # compute Accuracy Score
        for i in range(len(Predicted_values)):
            acc = accuracy_score(Actual_values[i], Predicted_values[i])
            print(f'Accuracy score calculated...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} =', acc, '\n')

            # Calculate & plot confusion matrix
            cm = confusion_matrix(Actual_values[i], Predicted_values[i])
            print(f'Confusion Matrix calculated...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} =', cm, '\n')
            heatmap = sns.heatmap(cm, annot=True, cmap='viridis', fmt='d')
            heatmap.set_title(self.name, fontsize=16)
            heatmap.set_xticklabels([f'No {self.name}', f'{self.name}'])
            heatmap.set_yticklabels([f'No {self.name}', f'{self.name}'])
            plt.savefig(f'{os.path.join(self.storage_path, "Confusion-Metrices", self.name + "_" + self.predicted_attribute[i])}.jpg', format='jpg')

            # Calculate Precision, Recall & F1 Score
            precision = precision_score(Actual_values[i], Predicted_values[i])
            recall = recall_score(Actual_values[i], Predicted_values[i])
            f1score = f1_score(Actual_values[i], Predicted_values[i])

            print(f'Confusion Matrix calculated...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} =', precision, '\n')
            print(f'Confusion Matrix calculated...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} =', recall, '\n')
            print(f'Confusion Matrix calculated...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} =', f1_score, '\n')
            print('All these metrices have been written into txt file as well.')
            
            # write all the calculated metrices into the file
            with open(f'{os.path.join(self.storage_path, "QA-Report", "QA-Report.txt")}', 'a') as f:
                f.write(f'Accuracy score calculated for...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} = {acc}\n')
                f.write(f'Precision score calculated for...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} = {precision}\n')
                f.write(f'Recall score calculated for...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} = {recall}\n')
                f.write(f'f1-score calculated for...\nTrue: {self.true_attribute[i]} & Predicted: {self.predicted_attribute[i]} = {f1score}\n\n')


if __name__ == "__main__":
    true_labels = sys.argv[1]
    true_attribute = sys.argv[2]
    predicted_labels = sys.argv[3]
    predicted_attribute = sys.argv[4]
    matrix_name = sys.argv[5]
    
    Evaluate(true_labels, true_attribute, predicted_labels, predicted_attribute, matrix_name)
    