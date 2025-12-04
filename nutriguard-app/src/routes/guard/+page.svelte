<script lang="ts">
import { onMount } from "svelte";

interface Food {
    food_id: number;
    name: string;
    category: string;
    kcal: number;
    protein: number;
    nacl: number;
    potassium: number;
    phosphate: number;
}

let foods: Food[] = [];
let query = "";
let filteredFoods: Food[] = [];
let selectedFood: Food | null = null;
let amount = 0;

// Nur im Browser ausführen
onMount(async () => {
    try {
        const res = await fetch('/api/foods', {method:"POST"});
        if (!res.ok) throw new Error('Fehler beim Laden der Daten');
        foods = await res.json();
    } catch (err) {
        console.error(err);
    }
});

// Filterfunktion
function updateResults() {
    filteredFoods = query
        ? foods.filter(f => f.name.toLowerCase().includes(query.toLowerCase()))
        : [];

    // Wenn noch nichts ausgewählt ist, setze das erste Ergebnis automatisch
    if (!selectedFood && filteredFoods.length > 0) {
        selectedFood = filteredFoods[0];
    }
}

// Auswahl eines Elements
function selectFood(food: Food) {
    selectedFood = food;
    query = food.name;
    filteredFoods = [];
    //console.log(selectedFood);
}

// Berechnung der Nährstoffwerte
function calculateNutrients() {
    //console.log(amount);
    if (!selectedFood || amount <= 0) return null;
    const factor = amount / 100;
    return {
        kcal: selectedFood.kcal * factor,
        protein: selectedFood.protein * factor,
        nacl: selectedFood.nacl * factor,
        potassium: selectedFood.potassium * factor,
        phosphate: selectedFood.phosphate * factor
    };
}

async function commitSubmission() {
    let dt_current: Date = new Date();
    let dt_string = dt_current.toISOString();
    let payload = {
        datetime: dt_string,
        user_id: "0x0x0x0",
        food_id: selectedFood?.food_id,
        amount: amount
    };
    console.log(JSON.stringify(payload, null, 2));

    try {
        const res = await fetch('http://127.0.0.1:8000/api/submitfood', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        console.log('Serverantwort:', data);
    } catch (err) {
        console.error('Fehler beim Senden:', err);
    }
}

$: nutrients = calculateNutrients();
</script>

<div class="grid grid-rows justify-center gap-y-6">
    <div class="text-2xl font-semibold">Mahlzeit eintragen</div>
    <div class="grid grid-rows gap-y-2">
        <div class="text-xl">1. Mahlzeit Suchen</div>
        <div class="input-group grid-cols-[auto_1fr_auto] relative">
            <input
                class="ig-input"
                type="search"
                placeholder="Hier Suchbegriff eingeben"
                bind:value={query}
                on:input={updateResults}
            />
            {#if filteredFoods.length > 0}
            <ul class="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded shadow z-10 max-h-48 overflow-y-auto">
                {#each filteredFoods as food}
                <li class="p-2 hover:bg-gray-100 cursor-pointer" on:click={() => selectFood(food)}>
                    {food.name}
                </li>
                {/each}
            </ul>
            {/if}
        </div>
    </div>

    <div class="grid grid-rows gap-y-2">
        <div class="text-xl">2. Menge angeben (Gramm)</div>
        <input
            class="input"
            type="number"
            min="0"
            placeholder="Menge in Gramm (g)"
            bind:value={amount}
            on:input={() => {
            if (selectedFood) {
                nutrients = calculateNutrients();
            }
        }}
        />
    </div>
    

    {#if nutrients}
    <div class="grid grid-rows gap-y-2">
        <div class="text-xl">3. Werte überschauen</div>
        <div class="p-2 border rounded">
        <div><strong>{selectedFood?.name}</strong> ({amount} g)</div>
        <ul class="mt-1">
            <li>Kcal: {nutrients.kcal.toFixed(1)}</li>
            <li>Protein: {nutrients.protein.toFixed(1)} g</li>
            <li>NaCl: {nutrients.nacl.toFixed(1)} g</li>
            <li>Potassium: {nutrients.potassium.toFixed(1)} mg</li>
            <li>Phosphate: {nutrients.phosphate.toFixed(1)} mg</li>
        </ul>
        </div>
    </div>
    
    <div class="mt-2">
        <a href="/guard" on:click={() => commitSubmission()}>Absenden</a>
    </div>
    {/if}
</div>
