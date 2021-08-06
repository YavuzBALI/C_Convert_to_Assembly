import os

"""                         Fonksiyon oluşturma                """
def create_Function(dosya_kopyasi,satir,eleman,degikenler_kopyasi,dongu_2,dongu_2_2):  #her bir fonksiyon bu fonksiyonda assemblye döndürülür, geri dönüş olarak bloğun bitiş satırını döner
    suslu_parantez =0                    #Bir blokta if else for lardan dolayı süslü parantez kapama bulunabilir bu değişken toplam süslü parantezi kontrol eder
    stringkopya=""                       #ilk string ataması yapılır daha sonra taramada ki stringler şartları kontrol etmek için bu değişken kullanılır
    if dongu_2==0:
        fonksiyon_ismi = dosya_kopyasi[satir][0:(eleman)]
        assembly.write(fonksiyon_ismi+":"+"\n")                #assembly de function label yazdırma
    if dongu_2!=0:
        dongu_label=dongu_sayisi_2*2-(dongu_2-1)
        assembly.write(".L"+str(dongu_label)+":"+"\n")
    string_sayisi=0
    ikinci_dongu=1
    degisken_sayisi=0                    #total değişken sayısı
    st=satir                             #süslü parantez satırından başlamak için
    hece=eleman                        #ilk süslü parantezden başlamak için
    dongu=1
    dongu_sayisi=dongu_2
    dongu_sayisi_2=dongu_2_2
    dongu_son_parantez=0
    while (ikinci_dongu==1):
        if st>satir:                    #süslü parantezin öncesini okumamak için kullanılır
            hece=0                       #ilk satırdaki süslü parantezin öncesi okunmadıktan sonra diğer satırlarda satır başına geçmek için
        for q in range(hece,len(dosya_kopyasi[st])):     #tarama döngüleri
            stringkopya=""                               #her taramada stringkopya yeni kelimeler için boşaltılır
            for e in range(q,len(dosya_kopyasi[st])):
                stringkopya+=dosya_kopyasi[st][e]        #kelimeler karşılaştırılmak üzere string kopyaya atanır
                if stringkopya == "}":                   #süslü parantezlerin sayısı denetlenir
                    suslu_parantez = suslu_parantez - 1
                if stringkopya == "{":
                    suslu_parantez = suslu_parantez + 1
                    if dongu==1:
                        dongu_sayisi_2+=1
                    if dongu==0 and suslu_parantez==2:
                        if_komutu=dosya_kopyasi[st].find("if")
                        for_komutu=dosya_kopyasi[st].find("for")
                        if  if_komutu>=0:
                            dongu_sayisi=dongu_sayisi+1
                            st=if_dongu(dosya_kopyasi,st,e,degikenler_kopyasi,dongu_sayisi,dongu_sayisi_2)
                            hece=0
                            suslu_parantez=suslu_parantez-1
                        if  for_komutu>=0:
                            dongu_sayisi=dongu_sayisi+1
                            st=for_komutu(dosya_kopyasi,st,e,degikenler_kopyasi,dongu_sayisi,dongu_sayisi_2)
                            suslu_parantez=suslu_parantez-1
                if  suslu_parantez==0:                          #eğer nihai süslü parantez sayısı sıfır ise tüm döngülerden çıkılır blok bitmiştir
                    st=satir
                    hece=eleman
                    if dongu==0:
                        ikinci_dongu=0                   #ikinci kez blok taranmıştır
                        assembly.write("    " + "sub.w" + " " + "#" + str((degisken_sayisi+1)*2) + " " + "SP" + "\n")  # değişken sayısını assembly olarak registerda hafıza açıl
                        break
                    if (dongu!=0):
                        dongu=0
                if stringkopya=="=" and ikinci_dongu==1 and dosya_kopyasi[st][e+1]!="=":                     #bloktaki eşittir durumuna karşın satır esittir_operandına eylemi işlemek için göndderilir
                    esittir_operandı(dosya_kopyasi[st],degikenler_kopyasi,e) #burada şimdilik neler döndürüleceği bilinmiyor

                if stringkopya=="int" and dongu==1 and dongu_sayisi==0:                         #eğer değişken tanımlaması var ise değişken sayısını saymak için degisken_sayici fonksiyonuna gönderilir
                    (degisken_sayisi,degikenler_kopyasi)=degisken_sayici(dosya_kopyasi,degikenler_kopyasi,st)

                    print(degikenler_kopyasi)
                    assembly.write("    " + "add.w" + "," + "#" + str((degisken_sayisi + 1) * 2) + " " + "SP" + "\n")  # değişken sayısını assembly olarak registerda açılan hafıza boşaltılır
            if suslu_parantez==0:
                break
        st+=1                                       #farklı satırları taramak için her döngüde diğer satıra geçer

    assembly.write("    " + "mow.b" + " " + "#0" + "," + "R12" + "\n")


    return (st,degikenler_kopyasi,dongu_2,dongu_sayisi_2)                             #En son kapalı parantezden sonrasını taramayı sağlamak için
"""                              Fonksiyon burda bitiyor                        """

"""                              Değişken sayısını tutuyoruz                   """
def degisken_sayici(dosya_kopyasi2,degiskenler_kopyasi_sayici,satir2): #satırda ki değişken sayısını sayar geri dönüş olara değişken sayısını int olarak döner
    degiskenler_iki=dosya_kopyasi2[satir2].replace("int","")
    degiskenler_iki=degiskenler_iki.strip()
    degiskenler_iki=degiskenler_iki.split(",")
    for sayac in range(len(degiskenler_iki)):
        degiskenler_iki[sayac]=degiskenler_iki[sayac].replace(";","")
        degiskenler_kopyasi_sayici.append(degiskenler_iki[sayac])

    return (len(degiskenler_iki),degiskenler_kopyasi_sayici)                    #virgülden bir fazla kadar değişken vardır
"""                            Fonksiyon burda bitiyor                           """

"""                            Eşittir Operadı                                   """
def esittir_operandı(dosya_esittir_satiri,degiskenler_kopyasi_esittir,hece_esittir):
    stg=""
    atanacak_olan=""
    atanan_konum=0
    kontol=hece_esittir+1
    pointer=hece_esittir
    operandlar=["+","*","-"]
    degisken_konum=0
    islem_yapıldı=0
    while (dosya_esittir_satiri[kontol]!=";" and islem_yapıldı==0):
        stg+=dosya_esittir_satiri[kontol]
        for sayac_iki in range(0,len(operandlar)):
            if dosya_esittir_satiri[kontol+1]==operandlar[sayac_iki]:
                for sayac_uc in range(0, (hece_esittir)):
                    atanacak_olan += dosya_esittir_satiri[sayac_uc]
                    atanacak_olan = atanacak_olan.strip()
                for sayac in range(0, len(degiskenler_kopyasi_esittir)):
                    if atanacak_olan == degiskenler_kopyasi_esittir[sayac]:
                        degisken_konum = (sayac+1) * 2
                        atanacak_olan = str(degisken_konum) + "(SP)"
                        assembly.write("    " + "mow.w" + " " +atanacak_olan+ " " + "R14"+"\n")
                islem_operandlari(dosya_esittir_satiri,(hece_esittir+1),degiskenler_kopyasi_esittir,"+")
                islem_yapıldı=1
                stg=""
        kontol+=1
    for sayac_uc in range(0,(hece_esittir)):
        atanacak_olan+=dosya_esittir_satiri[sayac_uc]
        atanacak_olan=atanacak_olan.strip()
    for sayac_dort in range(0,len(degiskenler_kopyasi_esittir)):
        if atanacak_olan==degiskenler_kopyasi_esittir[sayac_dort]:
            degisken_konum=(sayac_dort+1)*2
        if stg == degiskenler_kopyasi_esittir[sayac_dort] and stg!="":
            atanan_konum=(sayac_dort+1)*2
    if atanan_konum!=0 and islem_yapıldı==0:
        assembly.write("    "+"mow.w"+" "+str(atanan_konum)+"(SP)"+" "+str(degisken_konum)+"(SP)"+"\n")
        print(degiskenler_kopyasi_esittir)
    if atanan_konum==0 and islem_yapıldı==0:
        assembly.write("    "+"mow.w"+" "+"#"+stg+" "+str(degisken_konum)+"(SP)"+"\n")
    if islem_yapıldı==1:
        assembly.write("    " + "mow.w" + " " +"R14"+ " " + str(degisken_konum) + "(SP)" + "\n")

"""                                     Fonksiyon bitti                         """
"""                                     + ve - operandı                         """
def islem_operandlari(dosya_satiri_islem,pointer_operand,degisken_kopyasi_operand,operand):
    print(degisken_kopyasi_operand)
    kontrol=pointer_operand
    strng=""
    operandlar=["+","*","-"]
    ikincideger_konum=0
    ikincideger_strng=""
    if operand=="+":
        operan_koy="add.w"
    if operand=="-":
        operan_koy="sub.w"
    while (dosya_satiri_islem[kontrol]!=";"):
        strng+=dosya_satiri_islem[kontrol]
        print(strng)

        if operand=="*" and (dosya_satiri_islem[kontrol+1]=="-" or dosya_satiri_islem[kontrol+1]=="+" or dosya_satiri_islem[kontrol+1]==";"): # buradaki işlem eğer sağda daha fazla işlem varsa çarpma yap ve recursvele
                for sayac_bes in range(0,len(degisken_kopyasi_operand)):
                    if strng == degisken_kopyasi_operand[sayac_bes]:
                        ikincideger_konum = (sayac_bes+1) * 2
                        ikincideger_strng = str(ikincideger_konum) + "(SP)"
                    if sayac_bes == len(degisken_kopyasi_operand) and ikincideger_konum == 0:
                        ikincideger_strng ="#"+strng

                if dosya_satiri_islem[kontrol+1]!="*":
                    if dosya_satiri_islem[kontrol+1]!=";":
                        yeni_kontrol=kontrol+2
                        islem_operandlari(dosya_satiri_islem,yeni_kontrol,degisken_kopyasi_operand,dosya_satiri_islem[kontrol+1])
                    assembly.write("    "+"mow.w"+" "+ikincideger_strng+","+"R12"+"\n")
                    return

        for sayac in range(0,3):                     #toplamamı çıkarmamı diye bakıyor
            if dosya_satiri_islem[kontrol+1]==operandlar[sayac] or dosya_satiri_islem[kontrol+1]==";":
                print("ssssssssssssssssssssssssssssssss"+"           "+operandlar[sayac])
                for sayac_iki in range(0, len(degisken_kopyasi_operand)):
                    if strng == degisken_kopyasi_operand[sayac_iki]:
                        ikincideger_konum = (sayac_iki+1) * 2
                        ikincideger_strng = str(ikincideger_konum) + "(SP)"
                    if sayac_iki == len(degisken_kopyasi_operand) and ikincideger_konum == 0:
                        ikincideger_strng ="#"+strng

                if dosya_satiri_islem[kontrol+1]==";":
                    assembly.write("    " + operan_koy + " " + ikincideger_strng + " " + "R14" + "\n")
                    return

                yeni_kontrol = kontrol + 2
                islem_operandlari(dosya_satiri_islem, yeni_kontrol, degisken_kopyasi_operand,operandlar[sayac]) # recursive function
                if  dosya_satiri_islem[kontrol+1]=="*":
                    assembly.write("    " + "mow.w" + " " + ikincideger_strng + "," + "R13" + "\n")
                    assembly.write("    " + "CALL" + " " + "#__mspabi_mpyi" + "\n")
                    if operand!="*":
                        assembly.write("    "+operan_koy+" "+"R12"+","+"R14"+"\n")
                    return
                if dosya_satiri_islem[kontrol+1]!="*":
                    assembly.write("    " + operan_koy + " " + ikincideger_strng + " " + "R14" + "\n")
                    return
        kontrol+=1

"""                                             fonksiyon bitimi                              """
"""                                               for komutu                                   """
def for_komutu(dosya_kopyasi_for,pointer_for,pointer,degiskenler_kopyasi_for,dongu_sayisi_for,dongu_sayisi):
    assembly.write("    "+"br"+" "+".#L"+str(dongu_sayisi_for)+"\n")
    (pointer_for,degiskenler_kopyasi_for,dongu_sayisi_for,dongu_sayisi)=create_Function(dosya_kopyasi_for,pointer_for,pointer,degiskenler_kopyasi_for,dosya_kopyasi_for,dongu_sayisi)
    assembly.write(".#L"+str(dongu_sayisi_for)+":")
    stg=""
    kontrol=0
    operandlar=[">","<","="]
    while stg!=")":
        kontrol = kontrol + 1
        stg=dosya_kopyasi_for[pointer_for][kontrol]
        for sayac in range(0,3):
            if stg==operandlar[sayac]:
                if  stg=="=" and dosya_kopyasi_for[pointer_for][kontrol+1]=="=":
                    karsılastırm(dosya_kopyasi_for,degiskenler_kopyasi_for,pointer_for,kontrol,dongu_sayisi,operandlar[sayac],dongu_sayisi_for)
                if stg!="=":
                    karsılastırm(dosya_kopyasi_for, degiskenler_kopyasi_for, pointer_for, kontrol, dongu_sayisi,operandlar[sayac],dongu_sayisi_for)

    while stg!=";":
        kontrol=kontrol-1
        stg+=dongu_sayisi_for[pointer_for][kontrol]
        if dongu_sayisi_for[pointer_for][kontrol]!="=":
            stg=stg[::-1]
            if stg.find("+")>0:
                operand="add.w"
            if stg.find("-")>0:
                operand="sub.w"
            stg=stg.replace("+","")
            stg = stg.replace("-","")
            for sayac_iki in range(0,len(degiskenler_kopyasi_for)):
                if stg==degiskenler_kopyasi_for[sayac_iki]:
                    assembly.write("    "+operand+" "+"#1"+","+str(sayac_iki)+"(R14)"+"\n")
        if  dongu_sayisi_for[pointer_for][kontrol]=="=":
            for sayac_3 in range(0, len(degiskenler_kopyasi_esittir)):
                if atanacak_olan == degiskenler_kopyasi_esittir[sayac_3]:
                    degisken_konum = (sayac_3 + 1) * 2
                    atanacak_olan = str(degisken_konum) + "(SP)"
                    assembly.write("    " + "mow.w" + " " + atanacak_olan + " " + "R14" + "\n")
            islem_operandlari(dosya_esittir_satiri, (hece_esittir + 1), degiskenler_kopyasi_esittir,"+")
    kontrol=0
    while stg!="}":
        kontrol=kontrol+1
        for sayac_dort in range(0,len(dosya_kopyasi_for[kontrol])):
            stg=dosya_kopyasi_for[kontrol][sayac_dort]
            if stg=="}":
                return kontrol+1

def karsılastırm(dosya_kopyasi_kar,degiskenler_kopyasi_kar,pointer_kar,pointer,dongu_sayisi_kar,operand,dongusayisi_karma):
    kontrol=pointer
    if operand=="<":
        operan_koy="jge"
    if  operand==">":
        operan_koy="jl"
    if operand=="=":
        operan_koy="jeq"
        kontrol=kontrol+1
    sg=""
    sg_iki=""
    while dosya_kopyasi_kar[pointer_kar][kontrol+1]!=";":
        kontrol+=1
        sg+=dosya_kopyasi_kar[pointer_kar][kontrol]
        for sayac in range(0,len(degiskenler_kopyasi_kar)):
            if sg==degiskenler_kopyasi_kar[sayac]:
                degisken_konum=(sayac+1)*2
                degisken=str(degisken_konum)+sg
            if  sayac==len(dosya_kopyasi_kar) and dosya_kopyasi_kar[pointer_kar][kontrol+1]==";":
                degisken="#"+sg
    kontrol_2=0
    while dosya_kopyasi_kar[pointer_kar][kontrol - 1] != ";":
        kontrol -= 1
        sg += dosya_kopyasi_kar[pointer_kar][kontrol]
        for sayac_2 in range(0, len(degiskenler_kopyasi_kar)):
            if sg == degiskenler_kopyasi_kar[sayac]:
                degisken_konum_2 = (sayac + 1) * 2
                degisken_2 = str(degisken_konum) + sg
            if sayac == len(dosya_kopyasi_kar) and dosya_kopyasi_kar[pointer_kar][kontrol - 1] == ";":
                degisken_2 = "#" + sg
    assembly.write("    "+"mow.b"+" "+degisken+","+"R14")
    dongu_label = dongu_sayisi_kar * 2 - (dongusayisi_karma - 1)
    assembly.write("    "+"cmp.w"+" "+degisken_2+","+"R14"+"    "+"{"+" "+operan_koy+","+str(dongu_label))

"""                                              Fonksiyon bitimi                              """

string=" "                              #stringe eleman atamak işin boş bir string oluşturulur
dosya=input('Dosya ismini girin: ')     #dönüştürülmek istenen dosya ismi kullanıcıdan input alınır
C=open(dosya,"r")                       #okunacak dosya yolu açılır
assembly=open("Assembly.txt","w")       #Assembly olarak yazılacak dosya açılır

dosya_kodlari=C.readlines()
konum=0
degiskenler=[]
dongu_main=0
dongu_sayisi=-1
for i in range(0,len(dosya_kodlari)):
    for x in range(0,len(dosya_kodlari[i])):
        string =""
        for k in range(x,len(dosya_kodlari[i])):
            string+=dosya_kodlari[i][k]
            print(string)
            if string=="{":
                (konum,degiskenler,dongu_main,dongu_sayisi)=create_Function(dosya_kodlari,i,k,degiskenler,dongu_main,dongu_sayisi)    #en son bloğun bitiminden devam etmek için
                i=konum
                break
C.close()
assembly.close()