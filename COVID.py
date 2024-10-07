from tkinter import Tk, Checkbutton, IntVar, Button, Label, Toplevel
from experta import *

class Symptom(Fact):
    """Info about the symptoms."""
    pass

class CovidQuestionnaire(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []

    @Rule(Symptom(fever='alta'))
    def high_fever(self):
        self.recommendations.append("Tiene fiebre alta. Busque atención médica de inmediato.")

    @Rule(Symptom(fever='moderada'))
    def moderate_fever(self):
        self.recommendations.append("Tiene fiebre moderada. Descanse y controle la fiebre.")

    @Rule(Symptom(cough='persistente'))
    def persistent_cough(self):
        self.recommendations.append("Tiene tos persistente. Podría ser un síntoma de COVID-19.")

    @Rule(Symptom(breathing_difficulty='sí'))
    def breathing_difficulty(self):
        self.recommendations.append("Tiene dificultad para respirar. Busque atención médica urgente.")

    @Rule(Symptom(loss_of_senses='sí'))
    def loss_of_senses(self):
        self.recommendations.append("Ha perdido el sentido del olfato o del gusto. Esto es un síntoma común de COVID-19.")

    @Rule(Symptom(sore_throat='sí'))
    def sore_throat(self):
        self.recommendations.append("Tiene dolor de garganta. Esto podría estar relacionado con una infección viral.")

    @Rule(Symptom(headache='sí'))
    def headache(self):
        self.recommendations.append("Tiene dolor de cabeza. Controle los síntomas, especialmente si se acompaña de fiebre.")

    @Rule(Symptom(muscle_pain='sí'))
    def muscle_pain(self):
        self.recommendations.append("Tiene dolor muscular o corporal. Descanse y manténgase hidratado.")

    @Rule(Symptom(chills='sí'))
    def chills(self):
        self.recommendations.append("Tiene escalofríos. Podría ser un síntoma de infección viral.")

    @Rule(Symptom(fatigue='extrema'))
    def extreme_fatigue(self):
        self.recommendations.append("Tiene fatiga extrema. Descanse y monitoree sus síntomas.")

    @Rule(Symptom(congestion='sí'))
    def congestion(self):
        self.recommendations.append("Tiene congestión o secreción nasal. Esto es común en infecciones respiratorias.")

    @Rule(Symptom(nausea='sí'))
    def nausea(self):
        self.recommendations.append("Tiene náuseas o vómitos. Manténgase hidratado y consulte a un médico si persiste.")

    @Rule(Symptom(diarrhea='sí'))
    def diarrhea(self):
        self.recommendations.append("Tiene diarrea. Manténgase hidratado.")

    @Rule(
        OR(
            Symptom(fever='alta'),
            Symptom(breathing_difficulty='sí'),
            Symptom(loss_of_senses='sí')
        )
    )
    def severe_symptoms(self):
        self.recommendations.append("Es recomendable que se haga una prueba de COVID-19 inmediatamente y consulte a un médico.")

    @Rule(
        AND(
            Symptom(fever='moderada'),
            Symptom(cough='persistente')
        )
    )
    def moderate_risk(self):
        self.recommendations.append("Es recomendable que se haga una prueba de COVID-19 y permanezca en aislamiento preventivo.")

    @Rule(
        NOT(
            OR(
                Symptom(fever='alta'),
                Symptom(fever='moderada'),
                Symptom(cough='persistente'),
                Symptom(breathing_difficulty='sí'),
                Symptom(loss_of_senses='sí')
            )
        )
    )
    def no_test_needed(self):
        self.recommendations.append("Es poco probable que tenga COVID-19, pero siga monitoreando los síntomas y consulte a un médico si empeoran.")

def main():
    engine = CovidQuestionnaire()
    engine.reset()

    root = Tk()
    root.title("Cuestionario COVID-19")

    questions = {
        "fever": "¿Tiene fiebre? (alta, moderada, no)",
        "cough": "¿Tiene tos? (persistente, leve, no)",
        "breathing_difficulty": "¿Tiene dificultad para respirar?",
        "loss_of_senses": "¿Ha perdido el sentido del olfato o del gusto?",
        "sore_throat": "¿Tiene dolor de garganta?",
        "headache": "¿Tiene dolor de cabeza?",
        "muscle_pain": "¿Tiene dolor muscular o corporal?",
        "chills": "¿Tiene escalofríos?",
        "fatigue": "¿Tiene fatiga? (extrema, leve, no)",
        "congestion": "¿Tiene congestión o secreción nasal?",
        "nausea": "¿Tiene náuseas o vómitos?",
        "diarrhea": "¿Tiene diarrea?"
    }

    symptoms_vars = {key: IntVar() for key in questions.keys()}
    selected_symptoms = {}

    for key, question in questions.items():
        Checkbutton(root, text=question, variable=symptoms_vars[key]).pack(anchor='w')

    def submit():
        selected_symptoms.clear()
        symptoms = {key: 'sí' if var.get() == 1 else 'no' for key, var in symptoms_vars.items()}

        for key, value in symptoms.items():
            if value == 'sí':
                selected_symptoms[key] = questions[key]

        engine.recommendations.clear()  # Limpiar recomendaciones previas
        engine.declare(Symptom(**symptoms))
        engine.run()
#
        # Crear una nueva ventana para mostrar las recomendaciones
        result_window = Toplevel(root)
        result_window.title("Recomendaciones")
        Label(result_window, text="Resultados del cuestionario:").pack(pady=10)

        if engine.recommendations:
            for recommendation in engine.recommendations:
                Label(result_window, text=recommendation, wraplength=400, justify="left", font=("Arial", 10, "bold")).pack(anchor='w', padx=10)
        else:
            Label(result_window, text="No hay recomendaciones.", font=("Arial", 10, "bold")).pack(pady=10)

        Label(result_window, text="\nSíntomas seleccionados:", font=("Arial", 12, "bold")).pack(pady=5)
        if selected_symptoms:
            for key, symptom in selected_symptoms.items():
                Label(result_window, text=symptom, wraplength=400, justify="left").pack(anchor='w', padx=10)
        else:
            Label(result_window, text="No se seleccionaron síntomas.", wraplength=400, justify="left").pack(anchor='w', padx=10)

    Button(root, text="Enviar", command=submit).pack(pady=10)
    Label(root, text="Seleccione los síntomas que tiene y presione 'Enviar'", font=("Arial", 12, "bold")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
