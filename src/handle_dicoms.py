import numpy as np
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian

def save_dicom(image, info, filename):
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

    img = np.array(image.convert("L")).astype(np.uint8)

    dataset.Rows, dataset.Columns = img.shape
    dataset.SamplesPerPixel = 1
    dataset.PhotometricInterpretation = "MONOCHROME2"

    dataset.BitsAllocated = 8
    dataset.BitsStored = 8
    dataset.HighBit = 7
    dataset.PixelRepresentation = 0

    dataset.PixelSpacing = [1.0, 1.0]

    dataset.WindowCenter = 128
    dataset.WindowWidth = 256

    dataset.PixelData = img.tobytes()

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
        arr = np.frombuffer(dataset.PixelData, dtype=np.uint8)

        rows = getattr(dataset, "Rows", None)
        cols = getattr(dataset, "Columns", None)

        if rows and cols:
            image = arr.reshape(rows, cols)
        else:
            image = arr

    return info, image
