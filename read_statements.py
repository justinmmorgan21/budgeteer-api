import pdfplumber
import re
with pdfplumber.open("./BECU-Statement-21-Mar-2025.PDF") as pdf:
    for i in range(0, 8):
        page = pdf.pages[i]
        cropped = page.crop((0, 0.1 * float(page.height), page.width, page.height))
        page_text = cropped.extract_text()
        lines = page_text.splitlines()
        i = 0
        for line in lines:
            if re.search("^[0-9]+/[0-9]+/", line):
                index = line.find(" ")
                date = line[0 : index]
                line = line[index + 1 :]
                print("date:   " +  date)
                index = line.find(" ")
                amount = line[0 : index]
                line = line[index + 1 :]
                print("amount: $" +  amount[1 : len(amount) - 1])
                #line = line[line.find(" ") + 1 : ]
                print("payee:  " + line)
                print("-----------------------------------------------------")
                i = i + 1
    #print(page_text.find(" "))
