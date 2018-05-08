import requests

def main():
    r = requests.get("https://www.passport.gov.ph/appointment/individual/site")
    print(r.content)

if __name__ == "__main__":
    main()