import React from "react"

const IngredientCard = ({ ingredient }) => {
    return (
        <div className="ingredient">
            <div>
                <p>{ingredient.id}</p>
            </div>
            {/* <div>
                <img src={ingredient.Image !== 'N/A' ? ingredient.Image : 'https://via.placeholder.com/400'} alt={ingredient.Name} />
            </div> */}
            <div>
                <h2>{ingredient.name}</h2>
            </div>
        </div>
    )
}

export default IngredientCard;

