import { useState, useEffect } from "react";
import IngredientCard from "./IngredientCard";
import './App.css';
import SearchIcon from './searchIcon.svg';

const API_URL = '/';

const App = () => {
    const [ingredients, setIngredients] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    const searchIngredients = async () => {
        try {
            const response = await fetch(`${API_URL}ingredients`);
            const data = await response.json();
            setIngredients(data);
        } catch (error) {
            console.error('Error fetching ingredients:', error.message);
        }
    }

    useEffect(() => {
        searchIngredients();
    }, []);

    return (
        <div className="app">
            <h1>SearchBite</h1>
            <div className="search">
                <input
                    placeholder="What ingredients do you have in your fridge?"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <img
                    src={SearchIcon}
                    alt="search"
                    onClick={() => searchIngredients(searchTerm)}
                />
            </div>
            {
                ingredients?.length > 0
                    ? (
                        <div className="container">
                            {ingredients.map((ingredient) => (
                                <IngredientCard key={ingredient.id} ingredient={ingredient} />
                            ))}
                        </div>
                    ) :
                    (
                        <div className="empty">
                            <h2>No ingredients found</h2>
                        </div>
                    )
            }
        </div>
    );
}

export default App;
