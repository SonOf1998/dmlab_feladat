from bs4 import BeautifulSoup
from urllib.request import urlopen
from threading import Thread, Lock
import re
import sys
import pandas as pd
import numpy as np

URLS = ["https://www.hasznaltauto.hu/talalatilista/PCOG2U6RV3NDADH5S56ACFFYNTQXCE52JAJZUNDJV6K2DJUEEYYUVUXKALRN7ZZUUW2IZJ2YY53HY7DSAJZLNFBXF6TZSFAVAQWMSKOYMIRVNDCNUXYFONFIF5IAO2VBXEKKBR4F3MHD6KSXMBAN6QAB7YVFMOZZ5EXGSGGW4BZKG3CXHYCODKYDC5JGB3PS76VV6E35I6OMVMZM5CIJ7QEZXLSSRRNUHWLVFFHAYDXBK2HF34KGI4J72BSN7ZDY4YHB32RDAZ5JH3XXUU2ZYAU4UBRTJEPCYASFTAKNIHHWKO3MVRAA6PXWMHBA47NNQOHTHGC5GZUYO7L3CX3YO54HU43CZQJHDH6IHLSRPP2CTEPRQB662A4ZL7FIPX4OBQCUK5STUT2EPW7WO6Z63NSKQO7EXIP43KSR4ZOLWXJACXPKMAJAMXAFXHVK5YDCIMCWVXJDLQJNJOPWE7KPCOWW4JQSG3CYIIEOH7L3OCYH7JI2CVRPXNT3UABTWL4EZIGFUR7IUOL5TVHMKWYBOKH33NAGWOCTCAVZAC3ZKPEZB3ITFI4U24IW4MWMLMYYZ5JDZD7RHTCQXMN2OMYGHTOQS3UGUN64MQGPPXXEHZ3AMVJZLPGMBE32VXI6GCDF5KWJQRTTUUVFFZNKLMVWN7DVAYBAZX4IRPE7W26F32WIN6CHPQ5DVKFP2GBTFCQ2VMIJ7X7HWDJTA2UKGN2M2PVU5ICQ42GOOH3ORNXWX5CJOXJLWKLWNGDDCHIJ6X4IGZSOSSEOZIQ34TC7T776KEDFDNLVVGORVLYQH4ZUWQL7J6MBLQE5UDDY32J4Q3HDT62K6DO2AHM7WP6VKGDZ6"
      ,"https://www.hasznaltauto.hu/talalatilista/PCOG2U63R3NDAEH5C57QDYNSWTTLCERKKKCVMWVJV7IUBBTAGK3FPNQTOWB7R54O4MWJWZHTQAMJ3Y5ZTU4QDOL2SF3S7M5FCQKQILFNKNYMIRXMDBNTHJX4CV6GXTINTSXD6UNA6HNWHD27SUVTBIDPUDQCJMJ3ZFCWIMRJDKDASXFOSWEUKFSSRAUQH74GZRDAVLC5H3FDXTQRGHW5TH53DKQJA72NFNC5N7LPUUUMDAJZFMQOKZY6WAAL4BNSM2DOHHRHOREFODDWQZ7G43XXOAFXBA36ELPOLQSDWILIPQXWLD3MIBR3BXA467LYMCD35JXAMMHZ43VZ5CNP3GGK7TF3XS4XGYWMC35L6EGV3I6O5AJ3DZAG47NAPK77FAPV5HOVGYUGWDSFUJP3VNF7Q5RV7ZVHCTFO6XL2VVGLSVYU2ASZFW3LOAK6JKQYTSFTHNBNSCUIH63XIG65P7UGGQ4TQNVMECCBSKZ4TGIRLNWRQWGQVY2CFTEKKDRWQRFE6K4NVBISSHVTNZIYH6MAOLOADCHA3UDLCA5ZSF3ZK7G33VL4SLGFZMMC6U54RLYSVRPLDCXVHPARXMDQOKYWCRGYTLTW373BY43D2PZXYDRK2Y5OPX6FS3PVLGT3GFOZCJJH2SW23YRWNTBHW5YNMBETIBHITWN4ZRCJM42MCANV4CDEYPBIA2QAXGUPEG7E2HZMP5EEGNEWU6NC23GUCBTDWVVEGRGAUEEWVWDWVCFSFBYPEU6ER5DMVWFGJBMIK2C7T7BYTBRVD2H762DZPZWQ"
      ,"https://www.hasznaltauto.hu/talalatilista/PCOG2VG3R2NTAEH5C57UDSFF3U5I7FKWDOUYUKSV5IVZUJATOBWJQ2DMKCLSR766GGYASEA6CCRTH57DMOBV5PPJTPL4SURLBMATGYQDPOWNKVVQISVRY7CD4UC3RKC2NCWRLOEXYCKVMALT4QGK7I6Q3TYASA72DJHFER3NB55NDV5NAV3MA2LBZIMLZUCKJU67A37I3FUIKFNHUO6P3HBDU3W376SL24JFYSE7KNUZLNH755NGLQCQDYGTRY3HAKCBBX4AUNZMMJZ5B7EOQ4QMGTRX43CO55YAS4EBPYRNTZJMIMFBPOYT6VMPFQAGHMG4DL35MRQEMX5Z4BRQ7GLOXFUJXPKNNH7OT6P44RDCR6FAAL7SBV7GRC7HGLFFYGY7FAMKL7DIPX2MAUCUHZPO2S437NLJP537XPWMB6WYY77HF3NJJWN3OEA7SOPLIAIWU23UEKYEYVIALNEM22LQRKBAM45N7QC53ZGUWELBUIOM5DQ6CGPJIHMLBJRWMFOEQWBZK6AUFMGFWTJMQNJKEXNVKDIWKB7EENWMCBIQWLOEFH4SNAH3DR3QPZ7AJJAW2QLP6TGXJQTOAXIBCIHWGLNMXTS6IV55LWPLNCXTW65DW3324V4OMWDFZ4ILA5R576CWYTVXQCLEIWUQKDAEEQ5TCWBZURKL4M3FV7GM4RKMNGIWG4SYGRSOHFVC3ZNYXSXGERKKF3ZVX7UBS4MYOGK5CECNIRE6I7LD4WZNQNEPS5QZIFIFNKU3SUQZJTNHRQ6NFBOZVVKUKJHEZWIEZ4QQ5YJMB3YVRTMZAKDJRMAHT2TUHIKDDOROY7IKA4DXNMSKPRGOI3LYUL37W774ICP2W"
]

url_type = ["szemelyauto", "kishaszongepjarmu", "haszongepjarmu"]

dataframe = pd.DataFrame({
                    "BRAND": pd.Series([], dtype="str"),
                    "JARMU JELLEGE": pd.Series([], dtype="str"),
                    "UZEMANYAGTIPUS": pd.Series([], dtype="str"),
                    "EVJARAT": pd.Series([], dtype="int"),
                    "HENGERURTARTALOM (CM3)": pd.Series([], dtype="int"),
                    "TELJESITMENY (LE)": pd.Series([], dtype="int"),
                    "FUTOTT KILOMETER": pd.Series([], dtype="int"),
                    "AR (HUF)": pd.Series([], dtype="int"),
                })


# mennyi talalati lapon megyunk vegig egy tipus eseten
MAX_DEPTH = 10000
MULTITHREADED = True

lock = Lock()
def parse_raw_html(raw_html, car_type, depth=np.inf):
    soup = BeautifulSoup(raw_html, "lxml")

    vehicles = soup.find_all("div", {"class": re.compile("row talalati-sor.*")})
    for vehicle in vehicles:
        # a hirdetések első szava az autómárka
        # a mercedes esetében ez lehet mercedes-benz, mercedes-amg
        brand = vehicle.find("a", {"href": re.compile(".*www.hasznaltauto.hu.*") }).text.split(" ", 1)[0]
        price = vehicle.find("div", {"class" : "vetelar"}).text

        if not any(char.isdigit() for char in price):
            # ár nélküli hírdetések / csak bérelhető járművek
            continue
        if "Ft" not in price:
            # más valutában volt az ár mint ft (euró főleg)
            continue
        price = int(price.replace("Ft", "").replace("\xa0", ""))

        info_block = vehicle.find("div", {"class" : "talalatisor-info adatok"})
        info_set = info_block.find_all("span")

        engine_type = info_set[0].text.replace(",", "")
        if any(char.isdigit() for char in engine_type):
            # üzemanyag típus hiányzott
            continue

        threshold = 5
        cc_i = 2
        hp_i = 4
        km_i = 5

        cylinder_capacity = np.nan
        if engine_type == "Elektromos":
            cylinder_capacity = 0
            # nehany elektromos autó mégis rendelkezik hengerurtartalom adattal (1-re beállítva)
            if len(info_set) < 6:
                threshold = 4
                cc_i = None
                hp_i = 3
                km_i = 4

        if len(info_set) < threshold:
            # Túl hiányos hirdetés előnézet
            continue


        year = int(info_set[1].text.split("/", 1)[0].replace("\s", "").replace(",", ""))
        if cc_i is not None and engine_type != "Elektromos":
            if "cm³" not in info_set[cc_i].text:
                #dizel/benzines jarmunel hianyzott a hengerurtartalom
                continue
            cylinder_capacity = int(info_set[cc_i].text.rsplit(" ", 1)[0].replace("\xa0", ""))
        horsepower = int(info_set[hp_i].text.split("LE", 1)[0].replace("\xa0", ""))

        kilometres = np.nan

        if len(info_set) == threshold and year == 2021:
            # kilóméter nélküli 2021-es autókról feltételezhető, hogy nem futottak még
            kilometres = 0
        if len(info_set) == threshold + 1 and "km" in info_set[km_i].text:
            # ha megvan a kilóméter infó akkor használjuk, de egyébként legyen na
            kilometres = int(info_set[km_i].text.rsplit("km", 1)[0].replace("\xa0", ""))

        if MULTITHREADED:
            lock.acquire()
        dataframe.loc[dataframe.shape[0]] = [brand, car_type, engine_type, year, cylinder_capacity, horsepower, kilometres, price]
        if MULTITHREADED:
            lock.release()

    next_url_button = soup.find("b", {"class": re.compile("lapozoNyilJobb.*")})
    if next_url_button.parent.name != "a" or depth == MAX_DEPTH:
        # eljutottunk a hirdetések legvégére vagy szeretnenk megallni
        return None

    next_url = next_url_button.parent["href"]
    return next_url


def thread_fun(args):
    i = args[0]
    url = args[1]
    page = 1
    while url is not None:
        connection = urlopen(url)
        raw_html = connection.read()
        connection.close()
        try:
            url = parse_raw_html(raw_html, url_type[i], page)
            print("progress: {} (page {})".format(url_type[i], page))
            page = page + 1
        except ValueError as ve:
            print(ve, file=sys.stderr)
            print(url)
            exit(-1)


if __name__ == '__main__':
    if MULTITHREADED:
        threads = [None, None, None]
        for i, url in enumerate(URLS):
            threads[i] = Thread(target=thread_fun, args=([i, url], ))
            threads[i].start()

        for thread in threads:
            thread.join()
    else:
        for i, url in enumerate(URLS):
            page = 1
            while url is not None:
                connection = urlopen(url)
                raw_html = connection.read()
                connection.close()
                try:
                    url = parse_raw_html(raw_html, url_type[i], page)
                    print("progress: {} (page {})".format(url_type[i], page))
                    page = page + 1
                except ValueError as ve:
                    print(ve, file=sys.stderr)
                    print(url)
                    exit(-1)


    dataframe.to_csv("hasznaltauto_db.csv", index=False, encoding="utf-8-sig")
    print("done..")