import time
import asyncio
import streamlit as st
import pandas as pd

from core.db import add_request, add_serial_number
from core.utils import to_fixed, combine_serial_numbers
from core.loader import label_decoder, hardware_type_classifier, request_type_classifier


st.set_page_config(
    page_title="Оставить заявку",
    page_icon="👋",
)

st.write("# Диспетчеризация заявок")

with st.form("request_form"):
    st.header("Введите информацию о заявке")

    theme = st.text_input("Тема")
    description = st.text_area("Описание")
    submitted = st.form_submit_button("Отправить")

    if submitted:
        with st.spinner('Пожалуйста, подождите...'):
            start_time = time.time()

            theme = theme.replace('_x000D_', '')
            description = description.replace('_x000D_', '')

            hardware_type, hardware_type_confidence = hardware_type_classifier.predict(theme, description)
            request_type, request_type_confidence = request_type_classifier.predict(theme, description)

            request_id = asyncio.run(add_request(theme, description, label_decoder.request_type_labels[request_type], 
                                                 str(request_type_confidence), label_decoder.hardware_type_labels[hardware_type], 
                                                 str(hardware_type_confidence)))

            serial_numbers = combine_serial_numbers(theme, description)

            for number in serial_numbers:
                asyncio.run(add_serial_number(request_id, number))

            serial_numbers_df = pd.DataFrame(serial_numbers, columns=['Серийный номер'])

            generation_time = time.time() - start_time

        st.subheader("Результаты предсказаний") 

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Предсказанный тип оборудования")
            st.metric(label="Тип оборудования", value=label_decoder.hardware_type_labels[hardware_type])
            st.metric(label="Уверенность", value=f"{to_fixed(hardware_type_confidence*100, 2)}%")

        with col2:
            st.markdown("#### Предсказанная точка отказа")
            st.metric(label="Точка отказа", value=label_decoder.request_type_labels[request_type])
            st.metric(label="Уверенность", value=f"{to_fixed(request_type_confidence*100, 2)}%")

        st.markdown("#### Время генерации")
        st.write(f"{generation_time:.2f} секунд")

        st.divider()  
        st.subheader("Серийные номера")
        if len(serial_numbers) > 0:
            st.dataframe(serial_numbers_df)
        else:
            st.text('Серийных номеров не обнаружено. Рекомендуется уточнить у пользователя!')
