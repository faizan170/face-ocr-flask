import cv2
import pytesseract
import re
from passporteye import read_mrz


class engine(object):
    def __init__(self):
        self.result = None

    def preprocess_image(self, image):
        scale_percent = 150
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        ret, thresh = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresh

    def process(self, image):
        raw_extracted_text = pytesseract.image_to_string(image, lang="eng")
        return raw_extracted_text

    def extract_passport_data(self, image_path):
        mrz = read_mrz(image_path)
        if mrz:
            return mrz.to_dict()
        return None

    def is_id_pattern(self, elem):
        words = elem.split(" ")
        id_number = ""
        is_id = False
        for word in words:
            if word.replace("-", "").isdigit():
                if len(word.replace("-", "")) >= 10:
                    id_number = word
                    is_id = True
                    break
        return id_number, is_id

    def get_name(self, elem):
        words = elem.replace(":", "").split(" ")
        final_word = ""
        start = False
        for word in words:
            if word.lower() == "name" and not start:
                start = True
                continue
            elif not start:
                continue
            if start:
                final_word = final_word+" "+word
        return final_word.strip()

    def extract_date(self, text):
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        matches = re.findall(date_pattern, text)
        if matches:
            return matches[0]
        return None

    def extract_alpha(self, text):
        return re.sub('[^a-zA-Z0-9]+', '', text)

    def process_text(self, text, passport_data=None):
        # Use passport_data for passport-specific fields if available
        if passport_data:
            return passport_data
        arr = text.split("\n")
        elem = arr[0]
        dict_results = {}
        count = 0
        for elem in arr:
            if 'tionality' in elem.lower() or 'nation' in elem.lower() or 'tional' in elem.lower() or 'nationality' in elem.lower():
                nationality = elem.replace(":", "")
                nationality = nationality.split(" ")
                nationality_final = ""
                for i in range(1, len(nationality)):
                    nationality_final = nationality_final+" "+nationality[i]
                dict_results['nationality'] = nationality_final.strip()
            elif elem.replace("-", "").isdigit() or self.is_id_pattern(elem)[1]:
                dict_results['id_number'] = self.is_id_pattern(elem)[0]
            elif "birth" in elem.lower():
                dob = elem.split(":")[-1].strip()
                final_dob = self.extract_date(dob)
                if final_dob:
                    dict_results['date_of_birth'] = final_dob
            elif 'sex' in elem.lower():
                dict_results['sex'] = elem.split(":")[-1].strip()
            elif "name" in elem.lower():
                dict_results['name'] = self.get_name(elem)
            elif "passport" in elem.lower() or "pass" in elem.lower():
                dict_results["passport_number"] = self.extract_alpha(elem)
            elif "surname" in elem.lower():
                dict_results["surname"] = self.get_name(elem)
            elif "mother" in elem.lower():
                dict_results["mother_name"] = self.get_name(elem)
            elif "place" in elem.lower() and "birth" in elem.lower():
                dict_results["place_of_birth"] = self.get_name(elem)
            elif "expiry" in elem.lower():
                expiry_date = elem.split(":")[-1].strip()
                final_expiry_date = self.extract_date(expiry_date)
                if final_expiry_date:
                    dict_results['date_of_expiry'] = final_expiry_date
            elif "issue" in elem.lower():
                issue_date = elem.split(":")[-1].strip()
                final_issue_date = self.extract_date(issue_date)
                if final_issue_date:
                    dict_results['date_of_issue'] = final_issue_date
            elif "issuing" in elem.lower() and "authority" in elem.lower():
                dict_results["issuing_authority"] = self.get_name(elem)
        return dict_results

    def __call__(self, image_path):
        self.image = cv2.imread(image_path)
        self.preprocessed_image = self.preprocess_image(self.image)
        raw_text = self.process(self.preprocessed_image)

        # Attempt to extract passport data using PassportEye
        passport_data = self.extract_passport_data(image_path)
        out = self.process_text(raw_text, passport_data)
        self.result = out