import os

import numpy as np
import pydicom
from PIL import Image
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian

def save_dicom(image_array, info, filename):
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    dataset = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

    dataset.SpecificCharacterSet = "ISO_IR 192"
    dataset.is_little_endian = True
    dataset.is_implicit_VR = False

    dataset.PatientName = info["PatientName"]
    dataset.PatientID = info["PatientID"]
    dataset.PatientBirthDate = info["PatientBirthDate"]
    dataset.PatientSex = info["PatientSex"]
    dataset.PatientWeight = info["PatientWeight"]
    dataset.PatientSize = info["PatientSize"]

    dataset.StudyInstanceUID = generate_uid()
    series_uid = generate_uid()
    dataset.SeriesInstanceUID = series_uid

    dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    dataset.SOPClassUID = file_meta.MediaStorageSOPClassUID

    dataset.StudyDate = info["StudyDate"]
    dataset.Modality = "OT"

    dataset.StudyDescription = info["StudyDescription"]

    dataset.SeriesNumber = 1
    dataset.InstanceNumber = 1

    dataset.ImageType = ["ORIGINAL", "PRIMARY", "AXIAL"]

    dataset.Rows, dataset.Columns = image_array.shape
    dataset.SamplesPerPixel = 1
    dataset.PhotometricInterpretation = "MONOCHROME2"

    dataset.BitsAllocated = 8
    dataset.BitsStored = 8
    dataset.HighBit = 7
    dataset.PixelRepresentation = 0

    dataset.PixelSpacing = [1.0, 1.0]

    dataset.WindowCenter = 128
    dataset.WindowWidth = 256

    dataset.PixelData = image_array.tobytes()

    dataset.save_as(filename, write_like_original=False)

def load_dicom(filepath):
    dataset = pydicom.dcmread(filepath)

    def get(tag, default="BRAK"):
        return getattr(dataset, tag, default)

    info = {
        "PatientName": str(get("PatientName")),
        "PatientID": str(get("PatientID")),
        "PatientBirthDate": str(get("PatientBirthDate")),
        "PatientSex": str(get("PatientSex")),
        "PatientWeight": str(get("PatientWeight")),
        "PatientSize": str(get("PatientSize")),

        "StudyDate": str(get("StudyDate")),
        "StudyDescription": str(get("StudyDescription"))
    }


    image = None

    if hasattr(dataset, "PixelData"):
        image_array = np.frombuffer(dataset.PixelData, dtype=np.uint8)

        rows = getattr(dataset, "Rows", None)
        cols = getattr(dataset, "Columns", None)

        if rows and cols:
            image = image_array.reshape(rows, cols)
        else:
            image = image_array

    return info, image


def load_image(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".dcm":
        return load_dicom(filepath)
    else:
        img = Image.open(filepath).convert("L")
        image_array = np.array(img).astype(np.uint8)

        info = {
            "PatientName": "BRAK",
            "PatientID": "BRAK",
            "PatientBirthDate": "BRAK",
            "PatientSex": "BRAK",
            "PatientWeight": "BRAK",
            "PatientSize": "BRAK",
            "StudyDate": "BRAK",
            "StudyDescription": "BRAK"
        }

        return info, image_array

#image_info, image_array = load_image("../data/input/Kolo.dcm")
#print(image_info)
