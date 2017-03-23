import urllib
import os
import sys
import re
import datetime
import codecs

# Global data - types of months etc
max_days = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
separators = ['.', '-', '/']
meta_tag_types = [r"AUTOR", r"DZIAL", r"KLUCZOWE_."]
whitespaces = r'(?: |^|\s|$)'
local = r'[a-zA-Z1-9!#$%&\'*+\-/=?\^_`{|}~]'
domain = r'[a-zA-Z1-9\-]'

# Function responsible for traversing each file
def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    # Get the meta tags so we don't search the whole file
    meta_tags = '\n'.join(re.compile('^<META NAME.+$', re.MULTILINE).findall(content))

    # Search for author name
    pattern = r'<META NAME="AUTOR" CONTENT="(.*?)">'
    r = re.compile(pattern)
    m = r.search(meta_tags)
    author = m.group(1)

    #Search for the section name:
    pattern = r'<META NAME="DZIAL" CONTENT="(.*)">'
    r = re.compile(pattern)
    m = r.search(meta_tags)
    section = m.group(1)

    #Search for key-words:
    pattern = r'<META NAME="KLUCZOWE_." CONTENT="(.*)">'
    r = re.compile(pattern)
    keywords = join_list(r.findall(meta_tags))

    # Get the actual arcicle
    article = ''.join(re.compile(r'<P([\s\S]*)<META NAME=\"AUTOR\"', re.MULTILINE).findall(content))

    # Search for sentences, discard shortcuts
    pattern = r'([a-zA-Z1-9]{4,}(?:\.|!|\?)+(?: |<.+?>*\n))'
    r = re.compile(pattern)
    m = r.findall(article)
    no_of_sentences_tmp = str(len(m))

    # Search for shortcuts
    pattern = r'(?:(?: |\n<.+?>*|\()([a-zA-Z][a-z]{0,2})\.(?: |\n|$))'
    r = re.compile(pattern)
    shortcut_list = list(set(r.findall(article)))
    #If need be download list of actual short polish words to differentiate between them and shortcuts
    #no_of_shortcuts = exclude_words_from_shortcuts(shortcut_list)
    no_of_shortcuts = str(len(shortcut_list))

    #Seatch for dates
    pattern = get_regexp_for_date()
    r = re.compile(pattern)
    date_list = r.findall(article)
    date_list = dates_to_common_format(date_list)
    date_list = list(set(date_list))
    no_of_dates = str(len(date_list))
    
    #Search for integers
    pattern = r'(?={0}((?:-?(?:3276[0-7]|327[0-5][0-9]|32[0-6][0-9][0-9]|3[0-1][0-9][0-9][0-9]|[0-2]?[0-9]?[0-9]?[0-9]?[0-9]))|-32768){0})'.format(whitespaces)
    r = re.compile(pattern)
    integer_list = r.findall(article)
    #print integer_list
    integer_list = list(set(integer_list))
    no_of_integers = str(len(integer_list))

    # Search for e-mails
    #pattern = r'((?: |\n|^)[a-zA-Z1-9!#$%&\'*+\-/=?^_`{|}~]+(?:.[a-zA-Z1-9!#$%&\'*+\-/=?^_`{|}~]+)+@[a-zA-Z0-9\-]+(?:.[a-zA-Z0-9\-])*.[a-zA-Z0-9\-]+\b(?: |\n|$))'
    pattern = r'(?={0}({1}+(?:\.{1}+)*@{2}+(?:\.{2}+)+){0})'.format(whitespaces, local, domain)
    r = re.compile(pattern, re.MULTILINE)
    email_list = r.findall(article)
    #print email_list
    email_list = list(set(email_list))
    no_of_emails = str(len(email_list))


    # Search for floats
    pattern = r'(?={1}(-?(?:{0}\.|{0}\.{0}|\.{0}|{0}\.{0}[eE][+-]{0})){1})'.format(r'[0-9]+', whitespaces)
    r = re.compile(pattern)
    float_list = list(set(r.findall(article)))
    no_of_floats = str(len(float_list))

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor:", author)
    print("dzial:", section)
    print("slowa kluczowe:", keywords)
    print("liczba zdan:", no_of_sentences_tmp)
    print("liczba ROZNYCH skrotow:", no_of_shortcuts)
    print("liczba ROZNYCH liczb calkowitych z zakresu int:", no_of_integers)
    print("liczba ROZNYCH liczb zmiennoprzecinkowych:", no_of_floats)
    print("liczba ROZNYCH dat:", no_of_dates)
    print("liczba ROZNYCH adresow email:", no_of_emails)
    print("\n")

def join_list(list):
    return ', '.join(list)

def get_single_digit_regex_unformatted(number):
    result = r''
    result = r'(?:[0-{0}])'.format(number)
    return result


def get_regexp_below_number(number):
    regexp = r''
    if (number < 10):
        regexp = r"(?:0[0-{0}])".format(number)
    else:
        first_digit = number / 10
        second_digit = number % 10
        regexp = r"(?:(?:{0}[0-{1}])|(?:[0-{2}][0-9]))".format(first_digit, second_digit, (first_digit - 1))
    

    return regexp

def get_regexp_for_date():
    regexp = r''
    for separator in separators:
        # key is month, value is days
        for key, value in max_days.iteritems():
            regexp += r'{0}{1}{2}{1}[0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]{1}{0}{1}{2}'.format(get_regexp_below_number(value), separator, get_regexp_below_number(key))
            regexp += r'|'
    return regexp[:-1]

def exclude_words_from_shortcuts(shortcut_list):
    link = "http://www.pfs.org.pl/trojki.php"
    page = urllib.urlopen(link)
    page_content = page.read()
    word_section = ''.join(re.compile(r'<div id=\'tabs-wszystkie\' class=\'regular\'>([\s\S]*)</div>\n</div>', re.MULTILINE).findall(page_content)).decode('utf-8')
    words = ' '.join(re.compile(r'(?: |\n|>|\b)([a-zA-Z]{3})(?: |\n|<|\b)', re.MULTILINE).findall(word_section))
    word_list = words.split()
    word_list = [x.lower() for x in word_list]
    shortcut_list = [x.lower() for x in shortcut_list]
    shortcut_list = [item for item in shortcut_list if item not in word_list]
    return shortcut_list

def dates_to_common_format(date_list):
    result = []
    for date in date_list:
        for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%Y/%d/%m', '%Y-%d-%m', '%Y.%d.%m'):
            try:
                result.append(datetime.datetime.strptime(date, fmt).strftime('%d %m %Y'))
            except ValueError:
                pass
    return result

# Main function called after the program is run
def main():
    try:
        path = sys.argv[1]
    except IndexError:
        print("Brak podanej nazwy katalogu")
        sys.exit(0)


    tree = os.walk(path)

    for root, dirs, files in tree:
        for f in files:
            if f.endswith(".html"):
                filepath = os.path.join(root, f)
                processFile(filepath)


if __name__ == "__main__":
    main()

