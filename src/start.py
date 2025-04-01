#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import xml.etree.ElementTree as ET
import requests
import zipfile
import re
import gesetz_xml
from colorama import Fore, Style


def download_zip_files():
    # Parse the XML file
    tree = ET.parse('index-gesetze.xml')
    root = tree.getroot()

    # items
    i = 0
    for items in root:
        # item
        for item in items:
            try:
                if item.tag == 'link':
                    print(f"Link: {i} {item.text}")
                    download_file(item.text, 'zips')
                    unzip_file(f'zips/{os.path.basename(item.text)}', 'zips')
            except Exception as e:
                print(f"Error: {e}")
        i = i+1


def list_files_in_folder(folder_path):
    arr = []
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' doesn't exist.")
        return
    
    if not os.path.isdir(folder_path):
        print(f"'{folder_path}' is not a directory.")
        return
    
    print(f"Files in '{folder_path}':")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            if file_path.endswith('.xml'):
                arr.append(file_path)
    return arr


def unzip_file(zip_file_path, extract_to_folder):
    os.makedirs(extract_to_folder, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)


def download_file(url, destination_folder):
    # Get the filename from the URL
    filename = os.path.basename(url)
    
    # Create the full destination path
    destination_path = os.path.join(destination_folder, filename)
    
    # Make sure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Download the file
    response = requests.get(url, stream=True)
    
    # Raise an exception for bad status codes
    response.raise_for_status()
    
    # Write the file to the destination
    with open(destination_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return destination_path


def main():
    download_zip_files()

    gxml = gesetz_xml.gesetz_xml()

    for file in list_files_in_folder('zips'):
        try:
            print("")
            
            print(f"{Fore.GREEN}#{Style.RESET_ALL}" * 80)
            gxml.set_file(file)
            print(gxml.get_law_info())
            print("")
            gxml.parse_all_norm_elements()
        except Exception as e:                    
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    

if __name__ == "__main__":
    main()