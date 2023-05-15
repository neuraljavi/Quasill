import torch
from torch import nn
from torchtext.data.utils import get_tokenizer
from diagnosticator.classifier import TransformerClassifier
from torchtext.vocab import Vocab
import numpy as np

D_MODEL = 256
NUM_HEADS = 2
D_FF = 994
NUM_ENCODER_LAYERS = 1
DROP_OUT = 0.1981394172245322
N_CLASSES = 385
MAX_LENGTH = 128
LEARNING_RATE = 0.0001

DISEASES = {
    0: "Spontaneous abortion",
    1: "Dental abscess",
    2: "Prescription drug abuse",
    3: "Acalasia",
    4: "Pigmentary acanthosis",
    5: "Stroke",
    6: "Transitional ischemic accident",
    7: "Acne",
    8: "Acromegaly",
    9: "Adenomyosis",
    10: "Aphasia",
    11: "Primary progressive aphasia",
    12: "Canker sores",
    13: "Agoraphobia",
    14: "Heat exhaustion",
    15: "Breast enlargement in men (gynecomastia)",
    16: "Liver enlargement",
    17: "Albinism",
    18: "Milk allergy",
    19: "Penicillin allergy",
    20: "Pet allergy",
    21: "Allergy to dust mites",
    22: "Seafood allergy",
    23: "Egg allergy",
    24: "Latex allergy",
    25: "Nickel allergy",
    26: "Sun allergy",
    27: "Wheat allergy",
    28: "Food Allergy",
    29: "Allergies",
    30: "Medication allergies",
    31: "Dry socket",
    32: "Amblyopia (lazy eye)",
    33: "Amenorrhea",
    34: "Tonsillitis",
    35: "Streptococcal tonsillitis",
    36: "Amyloidosis",
    37: "Amnesia",
    38: "Amnesia Global Transitor",
    39: "Anaphylaxis",
    40: "Anemia",
    41: "Aplastic anemia",
    42: "Sickle cell anemia",
    43: "Iron deficiency anemia",
    44: "Vitamin deficiency anemia",
    45: "Abdominal aortic aneurysm",
    46: "Cerebral Aneurysm",
    47: "Aortic aneurysm",
    48: "Thoracic aortic aneurysm",
    49: "Aneurysms",
    50: "Angina pectoris",
    51: "Angiosarcoma",
    52: "Congenital heart defects in children",
    53: "Ebstein anomaly",
    54: "Congenital heart disease in adults",
    55: "Anorexia nervosa",
    56: "Anorgasmia in women",
    57: "Appendicitis",
    58: "Central sleep apnea",
    59: "Sleep apnea",
    60: "Obstructive sleep apnea",
    61: "Obstructive sleep apnea in children",
    62: "Child speech apraxia",
    63: "Heartburn",
    64: "Cardiac arrhythmia",
    65: "Wrinkles",
    66: "Arteriosclerosis/atherosclerosis",
    67: "Giant cell arteritis",
    68: "Takayasu's arteritis",
    69: "Arthritis",
    70: "Thumb arthritis",
    71: "Psoriasic arthritis",
    72: "Reactive arthritis",
    73: "Rheumatoid arthritis",
    74: "Asbestosis",
    75: "Ascariasis",
    76: "Ashtma",
    77: "Exercise-induced asthma",
    78: "Occupational asthma",
    79: "Aspergillosis",
    80: "Astigmatism",
    81: "Glioma",
    82: "Heart attack",
    83: "Ataxia",
    84: "Atelectasis",
    85: "Pulmonary atresia",
    86: "Posterior cortical atrophy",
    87: "Multiple system atrophy (MSA)",
    88: "Vaginal atrophy",
    89: "Self harm/cuts",
    90: "Suicide and suicidal thoughts",
    91: "Barotrauma",
    92: "Enlarged spleen (splenomegaly)",
    93: "Blastocystis hominis",
    94: "Blepharitis",
    95: "Branch Block",
    96: "Goiter",
    97: "Bags under the eyes",
    98: "Botulism",
    99: "Bradycardia",
    100: "Bronchiolitis",
    101: "Bronchitis",
    102: "Brucellosis",
    103: "Bruxism (grinding of teeth)",
    104: "Bulimia nervosa",
    105: "Suspicious lumps in the breast",
    106: "Bursitis",
    107: "Hair Loss",
    108: "Heart murmurs",
    109: "Sweating and body odor",
    110: "Muscle Cramp",
    111: "Menstrual cramps",
    112: "Calciphylaxis",
    113: "Gallstones",
    114: "Bladder stones",
    115: "Kidney stones",
    116: "Calluses and calluses",
    117: "Cancer",
    118: "Tonsil cancer",
    119: "Anus cancer",
    120: "Mouth cancer",
    121: "Head and neck cancer",
    122: "H\u00fcrthle cell cancer",
    123: "Colon cancer",
    124: "Cervical cancer",
    125: "Endometrial cancer",
    126: "Esophagus cancer",
    127: "Stomach cancer",
    128: "Throat cancer",
    129: "Liver cancer",
    130: "Bone cancer",
    131: "Adrenal gland cancer",
    132: "Lip cancer",
    133: "Tongue cancer",
    134: "Breast cancer",
    135: "Inflammatory breast cancer",
    136: "Recurring breast cancer",
    137: "Ovarian cancer",
    138: "Pancreatic cancer",
    139: "Skin cancer",
    140: "Non melanoma skin cancer",
    141: "Prostate cancer",
    142: "Prostate cancer in stage 4",
    143: "Lung cancer",
    144: "Kidney cancer",
    145: "Thyroid cancer",
    146: "Ureter cancer",
    147: "Vagina cancer",
    148: "Bladder cancer",
    149: "Small intestine cancer",
    150: "Male breast cancer",
    151: "Rectal cancer",
    152: "Testicular cancer",
    153: "Vulvar cancer",
    154: "Oral thrush",
    155: "Vaginal yeast infection",
    156: "Carbuncle",
    157: "Basal cell carcinoma",
    158: "Merkel cell carcinoma",
    159: "Squamous cell carcinoma of the skin",
    160: "Ductal Carcinoma In Situ",
    161: "Invasive Lobular Carcinoma",
    162: "Nasopharyngeal Carcinoma",
    163: "Sleepwalking",
    164: "Dilated cardiomyopathy",
    165: "Hypertrophic cardiomyopathy",
    166: "Dental cavities",
    167: "Dandruff",
    168: "Cataracts",
    169: "Cluster headache",
    170: "Celiac disease",
    171: "Hot flashes",
    172: "Cellulitis",
    173: "Cervicitis",
    174: "Diabetic ketoacidosis",
    175: "Bedbugs",
    176: "Chlamydia trachomatis",
    177: "Sciatica",
    178: "Keloid Scars",
    179: "Cyclothymia (Cyclothymic Disorder)",
    180: "Kyphosis",
    181: "Cirrhosis",
    182: "Cystitis",
    183: "interstitial cystitis",
    184: "Claudication",
    185: "Kleptomania",
    186: "Aortic Coarctation",
    187: "Golfer's Elbow",
    188: "Tennis Elbow",
    189: "Cholangiocarcinoma (bile duct cancer)",
    190: "Primary biliary cholangitis",
    191: "Primary sclerosing cholangitis",
    192: "Cholecystitis",
    193: "Cholera",
    194: "Pregnancy cholestasis",
    195: "Ischemic colitis",
    196: "Microscopic colitis",
    197: "Clostridium difficile-associated diarrhea (CDAD)",
    198: "Ulcerative colitis",
    199: "Urine color",
    200: "Coma",
    201: "Diabetic Coma",
    202: "Atrioventricular Septal Defect",
    203: "Interventricular communication",
    204: "Chondrosarcoma",
    205: "Compulsive sexual behavior",
    206: "Persistent arterial duct",
    207: "Freezing",
    208: "Concussion",
    209: "Excessive use of headache medication",
    210: "Low sperm count",
    211: "Premature ventricular contractions",
    212: "Dupuytren's contracture",
    213: "Seizures",
    214: "Frontal lobe seizures",
    215: "Febrile seizures",
    216: "Dilated heart",
    217: "Spinal cord tumor",
    218: "Costochondritis",
    219: "Brain Tumor",
    220: "Craniosynostosis",
    221: "Cryoglobulinemia",
    222: "Absence seizure",
    223: "Congenital Myasthenic Syndromes",
    224: "Infant jaundice",
    225: "Impetigo",
    226: "Stress urinary incontinence",
    227: "Fecal incontinence",
    228: "Urinary incontinence",
    229: "Urinary tract infection",
    230: "Ear infection (middle ear)",
    231: "C. difficile infection",
    232: "Cytomegalovirus infection",
    233: "Giardia infection (giardiasis)",
    234: "Helicobacter pylori (H. pylori) infection",
    235: "Listeria infection",
    236: "Norovirus infection",
    237: "Intestinal parasite infection",
    238: "Salmonella infection",
    239: "MRSA Infection",
    240: "Tapeworm infection",
    241: "HPV infection",
    242: "Staphylococcal infections",
    243: "Influenza (Flu)",
    244: "Indigestion",
    245: "Primary immunodeficiency",
    246: "Insomnia",
    247: "Heart failure",
    248: "Cervical insufficiency",
    249: "Mitral valve failure",
    250: "Tricuspid valve failure",
    251: "Pseudocolinesterase insufficiency",
    252: "Acute liver failure",
    253: "Pituitary insufficiency",
    254: "Acute renal failure",
    255: "Aortic valvular insufficiency",
    256: "Lactose intolerance",
    257: "Alcohol intolerance",
    258: "Food poisoning",
    259: "Carbon monoxide poisoning",
    260: "Alcohol poisoning",
    261: "Lead poisoning",
    262: "Intussusception",
    263: "Intestinal ischemia",
    264: "Mesenteric ischemia",
    265: "Myocardial ischemia",
    266: "Small Bowel Bacterial Overgrowth",
    267: "Emotional lability",
    268: "Cleft lip and cleft palate",
    269: "Blocked tear duct",
    270: "Laryngitis",
    271: "Geographic tongue",
    272: "Black hairy tongue",
    273: "Traumatic brain injury",
    274: "Anterior Cruciate Ligament Injury",
    275: "Rotator cuff injury",
    276: "Brachial plexus injury",
    277: "Hamstring muscle injury",
    278: "Peripheral nerve injuries",
    279: "Spinal cord injuries",
    280: "Leukemia",
    281: "Hairy cell leukemia",
    282: "Acute lymphocytic leukemia",
    283: "Chronic lymphocytic leukemia",
    284: "Acute myeloid leukemia",
    285: "Chronic myeloid leukemia",
    286: "Leukoplakia",
    287: "Mesenteric lymphadenitis",
    288: "Lymphoedema",
    289: "Lymphoma",
    290: "Cutaneous T-cell lymphoma",
    291: "Hodgkin's lymphoma (Hodgkin's disease)",
    292: "Non-Hodgkin's lymphoma",
    293: "Soft tissue sarcoma",
    294: "Lipoma",
    295: "Liposarcoma",
    296: "Lichen Sclerosus",
    297: "Lichen Planus",
    298: "Oral Lichen Planus",
    299: "Panic attacks and panic disorder",
    300: "Headaches in children",
    301: "Ludopathy",
    302: "Lupus",
    303: "Syringomyelia",
    304: "Chilblains",
    305: "Sacroiliitis",
    306: "Gastrointestinal bleeding",
    307: "Blood in the urine (hematuria)",
    308: "Measles",
    309: "Sarcoidosis",
    310: "Sarcoma",
    311: "Ewing's Sarcoma",
    312: "Soft Tissue Sarcoma",
    313: "Paraneoplastic Syndromes of the Nervous System",
    314: "Acute Sinusitis",
    315: "Chronic Sinusitis",
    316: "Scabies",
    317: "Fibrocystic Breast Condition",
    318: "Septicemia",
    319: "Dry Mouth",
    320: "Idiopathic Intracranial Hypertension (Pseudotumor Cerebri)",
    321: "Syphilis",
    322: "Vasovagal syncope",
    323: "Fetal alcohol syndrome",
    324: "Antiphospholipid syndrome",
    325: "Chronic Exercise Compartment Syndrome",
    326: "Acute Coronary Syndrome",
    327: "Thoracic Outlet Syndrome",
    328: "Alfa-gal syndrome",
    329: "Angelman Syndrome",
    330: "Popliteal Artery Entrapment Syndrome",
    331: "Burning Mouth Syndrome",
    332: "Brugada Syndrome",
    333: "Toxic Shock Syndrome",
    334: "Churg-Strauss Syndrome",
    335: "Cushing's Syndrome",
    336: "Acute Respiratory Distress Syndrome",
    337: "DiGeorge Syndrome (22q11.2 Deletion Syndrome)",
    338: "Sinus Dysfunction Syndrome",
    339: "Myofascial Pain Syndrome",
    340: "Patellofemoral Pain Syndrome",
    341: "Complex Regional Pain Syndrome",
    342: "Down Syndrome",
    343: "Ehlers-Danlos Syndrome",
    344: "Rapid Gastric Emptying Syndrome",
    345: "Chronic Fatigue Syndrome",
    346: "Gilbert's Syndrome",
    347: "Guillain-Barr\u00e9 Syndrome",
    348: "Ovarian Hyperstimulation Syndrome",
    349: "Horner's Syndrome",
    350: "Irritable Bowel Syndrome",
    351: "Klinefelter's Syndrome",
    352: "Klippel-Trenaunay syndrome",
    353: "Serotonin syndrome",
    354: "Restless legs syndrome",
    355: "Lynch Syndrome",
    356: "Marfan Syndrome",
    357: "Sudden infant death syndrome (SMSL)",
    358: "Noonan Syndrome",
    359: "Polycystic Ovary Syndrome",
    360: "POEMS syndrome",
    361: "Prader-Willi Syndrome",
    362: "Long QT syndrome",
    363: "Ramsay Hunt syndrome",
    364: "Rett syndrome",
    365: "Reye's syndrome",
    366: "Rumination syndrome",
    367: "Sj\u00f6gren's syndrome",
    368: "Stevens-Johnson syndrome",
    369: "Stickler Syndrome",
    370: "Tourette Syndrome",
    371: "Turner Syndrome",
    372: "Solitary Rectal Ulcer Syndrome",
    373: "Cyclic vomiting syndrome",
    374: "Wolff-Parkinson-White syndrome",
    375: "Shaken baby syndrome",
    376: "Broken Heart Syndrome",
    377: "Midgut Volvulus Syndrome",
    378: "Carpal Tunnel Syndrome",
    379: "Myelodysplastic Syndromes",
    380: "Metabolic Syndrome",
    381: "Nephrotic syndrome",
    382: "Post-polio syndrome",
    383: "Premenstrual syndrome (PMS)",
    384: "Triple X syndrome"
}

# TODO: VOLVER A DEJAR ESTO COMO ESTABA...
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')


def tensor_to_percentages(tensor):
    # Convertir el tensor en un objeto numpy
    np_tensor = tensor.cpu().detach().numpy()
    # Convertir las probabilidades a porcentajes
    percentages = np_tensor * 100

    # Convert numpy array to list
    percentages = percentages.tolist()

    return percentages


def load_model(vocab):
    classifier = TransformerClassifier(d_model=D_MODEL, num_heads=NUM_HEADS, d_ff=D_FF,
                                       num_layers=NUM_ENCODER_LAYERS, input_dim=len(vocab),
                                       n_classes=N_CLASSES, max_length=MAX_LENGTH, droput=DROP_OUT)
    classifier.load_state_dict(torch.load('diagnosticator/model/model.pth', map_location=torch.device('cpu')))
    return classifier


def encode(text, tokenizer, vocab, max_length):
    # Tokeniza el texto
    tokenized_text = tokenizer(text)

    # Codifica el texto
    encoded_text = [vocab[token] for token in tokenized_text]

    # Añade padding
    if len(encoded_text) < max_length:
        encoded_text += [vocab['<pad>']] * (max_length - len(encoded_text))
    else:
        encoded_text = encoded_text[:max_length]
    return encoded_text


def update_model(model, user_input, correct_label, tokenizer, vocab):
    model.train()

    # Define el optimizador y la función de pérdida
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss()

    # Tokeniza y codifica el texto de entrada
    encoded_text = encode(user_input, tokenizer, vocab, MAX_LENGTH)
    input_tensor = torch.tensor(encoded_text).to(device)

    # Codifica la etiqueta correcta
    label_tensor = torch.tensor([correct_label]).to(device)

    # Calcula la salida del modelo
    logits = model(input_tensor)

    optimizer.zero_grad()

    # Calcula la pérdida
    loss = criterion(logits, label_tensor)

    # Realiza la retropropagación y actualiza los parámetros
    loss.backward()
    optimizer.step()

    torch.save(model.state_dict(), 'diagnosticator/model/model.pth')

    model.eval()

    return loss.item()


def predict(text):
    # Carga el modelo y el vocabulario
    tokenizer = get_tokenizer('basic_english')
    vocab = torch.load('diagnosticator/model/vocab.pkl')

    # Codifica el texto de entrada
    encoded_text = encode(text, tokenizer, vocab, MAX_LENGTH)

    classifier = load_model(vocab)

    # Mueve el modelo a la GPU si está disponible
    classifier.to(device)

    classifier.eval()

    # Convierte el texto codificado en un tensor de entrada
    input_tensor = torch.tensor(encoded_text).unsqueeze(0).to(device)

    # Calcula la salida del modelo
    with torch.inference_mode():
        logits = classifier(input_tensor)

    # Calcula las probabilidades
    #TODO VOLVER A DEJARLO IGUAL: probabilities = torch.softmax(logits, dim=-1).cpu().detach().numpy()
    probabilities = torch.softmax(logits, dim=-1).squeeze(0)
    probabilities = tensor_to_percentages(probabilities)

    # Crea un diccionario con las probabilidades de cada etiqueta
    prob_dict = {}

    # Asigna las probabilidades a cada etiqueta
    for i, prob in enumerate(probabilities):
        label = DISEASES[i]
        prob_dict[label] = prob

    # Devuelve el diccionario de probabilidades
    return prob_dict


def get_feedback(text, label):
    # Carga el modelo y el vocabulario
    tokenizer = get_tokenizer('basic_english')
    vocab = torch.load('diagnosticator/model/vocab.pkl')
    classifier = load_model(vocab)

    label_index = DISEASES[label]

    # Mueve el modelo a la GPU si está disponible
    classifier.to(device)
    classifier.eval()

    # Actualiza el modelo según el feedback
    loss = update_model(classifier, text, label_index, tokenizer, vocab)
    return loss
