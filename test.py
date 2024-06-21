prompt_list = ["Was ist net sales Jahresausblick für {} in 2024? gib mir eine zahl als antwort, ohne text", "Was ist der EBIT-Margen Ausblick von {}? gib mir nur eine Zahl als antwort, ohne text", "schreibe höchstens 150 Wörter und nur was speziefisch auf {} zutrifft."]

for x in prompt_list:
    company = "Siemens"
    x = x.format(company)
    print(x)
