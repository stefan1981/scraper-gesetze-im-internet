
import xml.etree.ElementTree as ET
from colorama import Fore, Style

class gesetz_xml:

    xml_file_path = ""

    def __init__(self):
        print("")
    
    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def process_multiline_string(self, text):
        text = str(text)
        lines = text.split('\n')
        trimmed_lines = [line.strip() for line in lines]
        result = ' '.join(trimmed_lines)
        return result

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def set_file(self, path):
        self.xml_file_path = path

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def get_law_info(self):
        result = {}
        result['filename'] =  self.xml_file_path

        tree = ET.parse(self.xml_file_path)
        root = tree.getroot()

        for norm in root[:1]:
            langue = norm.find("./metadaten/langue")
            jurabk = norm.find("./metadaten/jurabk")
            ausfertigung_datum = norm.find("./metadaten/ausfertigung-datum")

            if langue is not None:
               result['langue'] = self.process_multiline_string(langue.text)
            if jurabk is not None:
                result['jurabk'] = self.process_multiline_string(jurabk.text)
            if ausfertigung_datum is not None:
                result['ausfertigung_datum'] = self.process_multiline_string(ausfertigung_datum.text)
        return result

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def get_root_bjnr(self):
        """ get the doknr-attribute from the first norm element under the xml's root element """
        tree = ET.parse(self.xml_file_path)
        root = tree.getroot()
        for norm in root[:1]:
            return norm.attrib['doknr']

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def get_norm_type(self, doknr):
        """ get the type of the norm """
        if doknr == self.get_root_bjnr():
            return "FIRST_ELEMENT"
        if doknr.startswith(f"{self.get_root_bjnr()}BJNG"):
            return "STRUCTURE"
        if doknr.startswith(f"{self.get_root_bjnr()}BJNE"):
            return "ENTRY"
        return """XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Error in get_norm-type XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def parse_table(self, tgroup_element):
        """parse table and returns a list of rows"""
        rows = []        
        for row in tgroup_element.findall(".//row"):
            entries = row.findall("entry")
            if len(entries) == 2:  # Erwartet genau 2 Einträge pro Zeile
                col1_text = entries[0].text.strip() if entries[0].text else ""
                col2_text = entries[1].text.strip() if entries[1].text else ""
                rows.append((col1_text, col2_text))
        return rows

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    # def parse_dl(self, dl_element, indent=0):
    #     """process <DL> elements and their children recursively"""
    #     for child in dl_element:
    #         # if the child is a DT
    #         if child.tag == "DT":
    #             print("in DT")
    #             if child.text:
    #                 print(f"{' ' * indent}{child.text.strip()}")
    #             #else:
    #             #    print(f"{' ' * indent}{Fore.RED}DT No Text{Style.RESET_ALL}")
    #             #    print()

    #         # if the chhild is a DD
    #         elif child.tag == "DD":
    #             print("in DD")
    #             for sub_child in child:
    #                 if sub_child.tag == "LA":
    #                     print("in LA")
    #                     if sub_child.text:
    #                         print(f"{' ' * indent}{sub_child.text.strip()}")
    #                     else:
    #                         print(f"{' ' * indent}{Fore.RED}LA No Text{Style.RESET_ALL}")                        

    #                     # Falls ein weiteres DL-Element innerhalb von LA existiert, rekursiv aufrufen
    #                     nested_dl = sub_child.find("DL")
    #                     if nested_dl is not None:
    #                         self.parse_dl(nested_dl, indent + 4)
    #                 elif sub_child.tag == "DL":
    #                     # Falls DD direkt ein DL enthält, rekursiv aufrufen
    #                     self.parse_dl(sub_child, indent + 4)

    #         # if th child is a table
    #         elif child.tag == "tgroup":
    #             parsed_table = self.parse_table(child)
    #             for row in parsed_table:
    #                 print(f"{' ' * indent}{row[0]}  |  {row[1]}")


    def print_text(self, elem, indent):
        txt = ""
        tag = f"[{elem.tag}]"
        tag=""
        if elem.text:
            txt += f"{tag}{' ' * indent}{elem.text.strip()}"
            
        if elem.tail and elem.tail.strip():
            txt += f"{tag}{' ' * indent}{elem.tail.strip()}"
        return txt

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def parse_dl(self, elem, indent=0):
        """process <DL> elements and their children recursively"""

        #element has children
        if len(elem) > 0:
            #print(f"{Fore.YELLOW}{elem.tag} has {len(elem)} children{Style.RESET_ALL}")
            for child in elem:
                self.parse_dl(child, indent + 2)

        
        txt = self.print_text(elem, indent)
        if txt:
            print(f"{txt}")

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def parse_all_norm_elements(self):
        """ parse all norm elements under the xml-root"""
        tree = ET.parse(self.xml_file_path)
        root = tree.getroot()

        for norm in root:
            # structure elements
            if self.get_norm_type(norm.attrib['doknr']) == "STRUCTURE":
                print("-" * 80)
                structure_arr = []
                gliederungskennzahl = norm.find("./metadaten/gliederungseinheit/gliederungskennzahl")
                gliederungsbez = norm.find("./metadaten/gliederungseinheit/gliederungsbez")
                gliederungstitel = norm.find("./metadaten/gliederungseinheit/gliederungstitel")

                if gliederungskennzahl is not None:
                    structure_arr.append(self.process_multiline_string(gliederungskennzahl.text))
                    
                if gliederungsbez is not None:
                    structure_arr.append(self.process_multiline_string(gliederungsbez.text))

                if gliederungstitel is not None:
                    structure_arr.append(self.process_multiline_string(gliederungstitel.text))
                print(structure_arr)
            
            # entry elements
            if self.get_norm_type(norm.attrib['doknr']) == "ENTRY":
                # metadata of entry
                print("")
                entry_arr = []
                enbez = norm.find("./metadaten/enbez")
                titel = norm.find("./metadaten/titel")

                if enbez is not None:
                    entry_arr.append(self.process_multiline_string(enbez.text))

                if titel is not None:
                    entry_arr.append(self.process_multiline_string(titel.text))
                print(f"    {entry_arr}")

                # textdata of entry
                result = norm.find("./textdaten/text/Content")
                if result:
                    for P in norm.find("./textdaten/text/Content"):
                        self.parse_dl(P, 8)
                        #if P.text != None:
                        #    print(f"    {P.text}")

                        #for DL in P:
                        #    self.parse_dl(DL, 8)

    # ---------/---------/---------/---------/---------/---------/---------/---------/
    def get_node_details(self, node):
        print(f"Node: {node.tag}")
        print(f"Attributes: {node.attrib}")
        print(f"Text: {node.text}")
        print(f"Tail: {node.tail}")
