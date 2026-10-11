"use strict";

// Обновляет год в подвале; скрипт безопасен на страницах без этого элемента.
const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = String(new Date().getFullYear());
}
