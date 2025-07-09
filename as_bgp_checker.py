def es_as_privado(asn):
    return (64512 <= asn <= 65534) or (4200000000 <= asn <= 4294967294)

def main():
    print("Verificador de AS BGP")
    try:
        asn = int(input("Ingrese el número de Sistema Autónomo (AS): "))
        if es_as_privado(asn):
            print(f"El AS {asn} es PRIVADO.")
        else:
            print(f"El AS {asn} es PÚBLICO.")
    except ValueError:
        print("Error: debe ingresar un número entero válido.")

if __name__ == "__main__":
    main()