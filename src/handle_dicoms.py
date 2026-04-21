import os

import numpy as np
import pydicom
from PIL import Image
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian

def add_padding(image_array, pad_value=0):
    """returns square image array with padding added"""
    h, w = image_array.shape[:2]
    #Do większego wymiaru dopełniamy
    size = max(h, w)

    # Wypełniamy wartością pad value ( domyślnie zero)
    if len(image_array.shape) == 2:
        new_image_array = np.full((size, size), pad_value, dtype=image_array.dtype)
    else:
        new_image_array = np.full((size, size, image_array.shape[2]), pad_value, dtype=image_array.dtype)

    #Przesunięcia do wycentrowania obrazu
    y_offset = (size - h) // 2
    x_offset = (size - w) // 2

    #Oryginalny obraz wstawiamy w środek kwadratowego
    new_image_array[y_offset:y_offset + h, x_offset:x_offset + w] = image_array

    return new_image_array

def save_dicom(image_array, info, filename):
    """saves image array and info to filename"""
    #Metadane
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage #Typ obrazu
    file_meta.MediaStorageSOPInstanceUID = generate_uid() #ID obrazu
    file_meta.ImplementationClassUID = generate_uid() #ID implementacji
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian #Kodowanie danych little endian

    #Dataset
    dataset = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

    #Kodowanie znaków
    dataset.SpecificCharacterSet = "ISO_IR 192"
    dataset.is_little_endian = True
    dataset.is_implicit_VR = False

    #Dane pacjenta
    dataset.PatientName = info["PatientName"]
    dataset.PatientID = info["PatientID"]
    dataset.PatientBirthDate = info["PatientBirthDate"]
    dataset.PatientSex = info["PatientSex"]
    dataset.PatientWeight = info["PatientWeight"]
    dataset.PatientSize = info["PatientSize"]

    #ID badania i serii
    dataset.StudyInstanceUID = generate_uid()
    dataset.SeriesInstanceUID = generate_uid()

    #Powiązanie z metadanymi
    dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    dataset.SOPClassUID = file_meta.MediaStorageSOPClassUID

    #Dane badania
    dataset.StudyDate = info["StudyDate"]
    dataset.Modality = "OT" #Inny typ obrazu
    dataset.StudyDescription = info["StudyDescription"]

    #Numeracja
    dataset.SeriesNumber = 1
    dataset.InstanceNumber = 1

    #Typ obrazu
    dataset.ImageType = ["ORIGINAL", "PRIMARY", "AXIAL"]

    dataset.Rows, dataset.Columns = image_array.shape #Rozmiar obrazu
    #Obraz monochromatyczny
    dataset.SamplesPerPixel = 1
    dataset.PhotometricInterpretation = "MONOCHROME2"

    #8 bitowy obraz
    dataset.BitsAllocated = 8
    dataset.BitsStored = 8
    dataset.HighBit = 7
    dataset.PixelRepresentation = 0

    #Rozmiar piksela
    dataset.PixelSpacing = [1.0, 1.0]

    #Oknow wyświetlania
    dataset.WindowCenter = 128
    dataset.WindowWidth = 256

    #Zamiana na bajty
    dataset.PixelData = image_array.tobytes()

    #Zapis
    dataset.save_as(filename, write_like_original=False)

def load_dicom(filepath):
    """loads dicom image from filepath, return info and image"""
    dataset = pydicom.dcmread(filepath)

    #Funkcja pomocnicza do pobierania atrybutów
    def get(tag, default=None):
        return getattr(dataset, tag, default)

    #Słownik z informacjami
    info = {
        "PatientName": get("PatientName"),
        "PatientID": get("PatientID"),
        "PatientBirthDate": get("PatientBirthDate"),
        "PatientSex": get("PatientSex"),
        "PatientWeight": get("PatientWeight"),
        "PatientSize": get("PatientSize"),

        "StudyDate": get("StudyDate"),
        "StudyDescription": get("StudyDescription")
    }


    image = None

    #Pobranie obrazka
    if hasattr(dataset, "PixelData"):
        image_array = np.frombuffer(dataset.PixelData, dtype=np.uint8)

        rows = getattr(dataset, "Rows", None)
        cols = getattr(dataset, "Columns", None)

        #reshape do 2D
        if rows and cols:
            image_array = image_array.reshape(rows, cols)

        #Kwadratowy obraz
        image = add_padding(image_array)

    return info, image


def load_image(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".dcm":
        return load_dicom(filepath)
    else:
        img = Image.open(filepath).convert("L")
        image_array = np.array(img).astype(np.uint8)

        image_array = add_padding(image_array)

        #Brak danych, defaultowo None
        info = {
            "PatientName": None,
            "PatientID": None,
            "PatientBirthDate": None,
            "PatientSex": None,
            "PatientWeight": None,
            "PatientSize": None,
            "StudyDate": None,
            "StudyDescription": None
        }

        return info, image_array
