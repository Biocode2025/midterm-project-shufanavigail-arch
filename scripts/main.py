from pathlib import Path
def codon_seq(file): #פונקציה שמקבלת קובץ של רצפי דנא ומחזירה מילון של הקודונים, מספר רצפים שמתחלקים בשלוש, ואת הרצף החדש שכולל רק את הרצפים שמתחלקים בשלוש
    code_part = ''
    whole_code =''
    codon_dict = {}
    valid_seq_count = 0
    for line in file: # לולאה שבודקת האם הרצף עומד בתנאי (של להתחלק ב-3)
        line = line.strip('\n')
        line = line.upper()
        if line[0] != ">":
            code_part += line #אם השורה לא מתחילה ב< אז מוסיף למשתנה זמני את השורה
        if line[0] == ">" and code_part != '': #אם השורה כן מתחילה ב> והמשתנה הזמני לא ריק אז בודק את התנאי ברצף
            if len(code_part) % 3 == 0:
                whole_code += code_part
                valid_seq_count += 1 #אם הרצף מתחלק בשלוש מוסיף 1 למספר הרצפים התקינים
            code_part = ''
    if len(code_part) % 3 == 0: #בדיקת  התנאי לרצף האחרון
        whole_code += code_part
        valid_seq_count += 1 
    new_whole_code = whole_code.replace("T", "U") #מחליף את הT ברצף לU ובכך הופך את הרצף לרנא(צריך זאת מאחר והקודונים ברצף הם עם U)
    for i in range (0, len(new_whole_code), 3): #יוצר מילון שמפתחות הם הקודונים והערכים הם מספר ההופעות של כל קודון ברצף הגדול
        codon = new_whole_code[i:i+3]
        if codon in codon_dict:
            codon_dict[codon] += 1
        else:
            codon_dict[codon] = 1

    return new_whole_code, valid_seq_count, codon_dict

def Amino_codons(file, dict1, file2): #פונקציה שמקבלת שני קבצים ומילון וכותבת מידע על כל קודון בקובץ השני
    for line in file: 
        line = line.strip('\n')
        (Amino_Acid, sep, codons) = line.partition('\t') #מחלק כל שורה לחומצת אמינו וקודונים
        codon_list = codons.split(';') #מפריד את הקודונים אחד מהשני
        overall_appearance = 0
        for i in range (0, len(codon_list)): #מספר ההופעות של כל הקודונים מאותה חומצת האמינו שבודקים
            if codon_list[i] in dict1:
                overall_appearance += dict1[codon_list[i]]

        for i in range(0, len(codon_list)):
            if codon_list[i] in dict1:
              #בודק אם כל קודון במילון ומדפיס את חומצת האמינו, הקודון, מספר הופעות שלו והאחוז מתוך הקודונים שמקודדים לאותה חומצת אמינו
                print('%s %s %d %.1f%%' %(Amino_Acid, codon_list[i], dict1[codon_list[i]], dict1[codon_list[i]] * 100/ overall_appearance))
                file2.write('%s %s %d %.1f%%' %(Amino_Acid, codon_list[i], dict1[codon_list[i]], dict1[codon_list[i]] * 100/ overall_appearance)) # כותב את המידע שמדפיס לקובץ 2
                file2.write('\n')

#פתיחת קבצים
base = Path(__file__).resolve().parent.parent  # project root
data_dir = base / 'data'
results_dir = base / 'results'
codon_file = open(data_dir / 'AA_codons.txt', 'r')
yeast_file = open(data_dir / 'Yeast_cDNA_part.fa.txt', 'r')
Ecoli_file = open(data_dir / 'Ecoli_cDNA_part.fa.txt', 'r')
output_Ecoli = open(results_dir / 'Ecoli_codon_usage.txt', 'w')
output_yeast = open(results_dir / 'Yeast_codon_usage.txt', 'w')
#הרצף הגדול, מספר הרצפים התקינים ומילון הקודונים של השמר
whole_seq_yeast, valid_count_yeast, codon_dict_yeast = (codon_seq(yeast_file))

print('number of coding sequences in yeast: %d' %(valid_count_yeast))
output_yeast.write('Saccharomyces cerevisiae')
output_yeast.write('\n')
output_yeast.write('The number of coding sequences in yeast: %d' %(valid_count_yeast))
output_yeast.write('\n')
#שימוש בפונקציה שכותבת ומדפיסה את המידע על השמר
Amino_codons(codon_file, codon_dict_yeast, output_yeast)

codon_file.close()# סגירה ופתיחה של הקובץ כדי שיתאפשר להשתמש בו שוב
codon_file = open(data_dir / 'AA_codons.txt', 'r')
#הרצף הגדול, מספר הרצפים התקינים ומילון הקודונים של האיקולי
whole_seq_Ecoli, valid_count_Ecoli, codon_dict_Ecoli = (codon_seq(Ecoli_file))
print('number of coding sequences in Ecoli: %d' %(valid_count_Ecoli))
output_Ecoli.write('Escherichia coli')
output_Ecoli.write('\n')
output_Ecoli.write('The number of coding sequences in Ecoli: %d' %(valid_count_Ecoli))
output_Ecoli.write('\n')
#שימוש בפונקציה שכותבת ומדפיסה את המידע על האיקולי
Amino_codons(codon_file, codon_dict_Ecoli, output_Ecoli)
#סגירת הקבצים
codon_file.close()
yeast_file.close()
Ecoli_file.close()
output_Ecoli.close()
output_yeast.close()