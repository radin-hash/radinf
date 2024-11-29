from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys
import sqlite3

def get_tables():
    conn = sqlite3.connect(r'C:\Users\Asus\Desktop\python folder\quran.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, sura FROM quranNameList")
    tables = cursor.fetchall()
    conn.close()
    return tables

def make_ayat_with_meanings(ayat, meanings, show_meaning=False):
    s = ''
    for i, aye in enumerate(ayat):
        s += f"آیه {i + 1}: {aye[0]}\n"
        if show_meaning and i < len(meanings):
            s += f"معنی: {meanings[i][0] if meanings[i] else 'معنی موجود نیست'}\n\n"
    return s

def search_data(selected_sura, text_edit):
    conn = sqlite3.connect(r'C:\Users\Asus\Desktop\python folder\quran.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM quranNameList WHERE sura=?', (selected_sura,))
    sura_id = cursor.fetchone()[0]
    
    cursor.execute('SELECT text FROM quran_text WHERE sura=?', (sura_id,))
    sura_text = make_ayat_with_meanings(cursor.fetchall(), [])
    
    conn.close()
    text_edit.setPlainText(sura_text)
    text_edit.setProperty("showing_meaning", False)

def show_meaning(selected_sura, result_text):
    showing_meaning = result_text.property("showing_meaning")
    if showing_meaning:
        return

    conn = sqlite3.connect(r'C:\Users\Asus\Desktop\python folder\quran.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM quranNameList WHERE sura=?', (selected_sura,))
    sura_id = cursor.fetchone()[0]
    cursor.execute('SELECT text FROM quran_text WHERE sura=?', (sura_id,))
    ayat = cursor.fetchall()
    cursor.execute('SELECT text FROM fa_qaraati WHERE sura=?', (sura_id,))
    meanings = cursor.fetchall()
    text_with_meanings = make_ayat_with_meanings(ayat, meanings, show_meaning=True)
    
    conn.close()
    result_text.setPlainText(text_with_meanings)
    result_text.setProperty("showing_meaning", True)  

def u(button, result_text):
    current_style = result_text.styleSheet()
    if "background-color: #FFE934;" in current_style:
        result_text.setStyleSheet("color: white;"
                                  "background-color: #2E2E2E;"
                                  "selection-color: #2E2E2E;"
                                  "selection-background-color: white;")
        button.setText("تغییر به حالت روز")
    else:
        result_text.setStyleSheet("color: black;"
                                  "background-color: #FFE934;"
                                  "selection-color: #FFE934;"
                                  "selection-background-color: black;")
        button.setText("تغییر به حالت شب")

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("نرم افزار قرآني")
    window.setFont(QFont("IRRoya", 20))
    window.setGeometry(0, 0, 1350, 700)
    window.setStyleSheet("background-color: #ffcccb;")
    button = QPushButton("کلیک کن")
    
    main_layout = QVBoxLayout()
    form_layout = QHBoxLayout()
    
    tables = get_tables()
    table_combo = QComboBox()
    table_combo.addItems([t[1] for t in tables])
    table_combo.setFont(QFont("IRRoya", 18))
    form_layout.addWidget(QLabel("انتخاب سوره"))
    form_layout.addWidget(table_combo)
    table_combo.currentIndexChanged.connect(lambda: search_data(table_combo.currentText(), result_text))
    
    result_text = QTextEdit()
    result_text.setFont(QFont('Neirizi', 22)) 
    result_text.setStyleSheet("color: black;"
                              "background-color: #FFE934;"
                              "selection-color: #FFE934;"
                              "selection-background-color: black;")
    result_text.setReadOnly(True)
    result_text.setProperty("showing_meaning", False) 
    button.clicked.connect(lambda: u(button, result_text))
    
    button_show_meaning = QPushButton("نمایش معنی")
    button_show_meaning.clicked.connect(lambda: show_meaning(table_combo.currentText(), result_text))
    
    form_layout.addWidget(button_show_meaning)
    form_layout.addWidget(button)
    main_layout.addLayout(form_layout)
    main_layout.addWidget(result_text)
    
    container = QWidget()
    container.setLayout(main_layout)
    window.setCentralWidget(container)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()