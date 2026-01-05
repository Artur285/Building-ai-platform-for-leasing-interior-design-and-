"""AI-powered recommendation engine for building materials."""
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MaterialRecommender:
    """AI recommendation system for suggesting building materials."""
    
    def __init__(self):
        """Initialize the recommender."""
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
        self.material_vectors = None
        self.materials_data = []
    
    def fit(self, materials: List[Dict]) -> None:
        """
        Train the recommender with material data.
        
        Args:
            materials: List of material dictionaries with name, category, description, specs
        """
        self.materials_data = materials
        
        # Create text representations for each material
        material_texts = []
        for mat in materials:
            text_parts = [
                mat.get('name', ''),
                mat.get('category', ''),
                mat.get('description', ''),
                mat.get('specifications', '')
            ]
            material_texts.append(' '.join(filter(None, text_parts)))
        
        # Vectorize material descriptions
        if material_texts:
            self.material_vectors = self.vectorizer.fit_transform(material_texts)
    
    def recommend_by_project(self, project_description: str, 
                            project_type: str = None, 
                            top_n: int = 5) -> List[Tuple[Dict, float]]:
        """
        Recommend materials based on project description.
        
        Args:
            project_description: Description of the construction project
            project_type: Optional project type/category
            top_n: Number of recommendations to return
            
        Returns:
            List of tuples (material_dict, similarity_score)
        """
        if self.material_vectors is None or not self.materials_data:
            return []
        
        # Create query text
        query_text = project_description
        if project_type:
            query_text = f"{project_type} {query_text}"
        
        # Vectorize query
        query_vector = self.vectorizer.transform([query_text])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.material_vectors)[0]
        
        # Get top N indices
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        
        # Return materials with scores
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only return if there's some similarity
                recommendations.append((self.materials_data[idx], float(similarities[idx])))
        
        return recommendations
    
    def recommend_complementary(self, material_ids: List[int], 
                               top_n: int = 5) -> List[Tuple[Dict, float]]:
        """
        Recommend complementary materials based on selected materials.
        
        Args:
            material_ids: List of already selected material IDs
            top_n: Number of recommendations to return
            
        Returns:
            List of tuples (material_dict, relevance_score)
        """
        if self.material_vectors is None or not self.materials_data:
            return []
        
        # Find materials by ID
        selected_materials = [mat for mat in self.materials_data if mat['id'] in material_ids]
        
        if not selected_materials:
            return []
        
        # Get categories of selected materials
        selected_categories = set(mat.get('category', '') for mat in selected_materials)
        
        # Find complementary materials (different category but related)
        recommendations = []
        for idx, mat in enumerate(self.materials_data):
            if mat['id'] not in material_ids:
                # Calculate relevance based on category diversity and similarity
                category_score = 0.5 if mat.get('category') not in selected_categories else 0.2
                
                # Average similarity to selected materials
                mat_vector = self.material_vectors[idx:idx+1]
                selected_indices = [i for i, m in enumerate(self.materials_data) if m['id'] in material_ids]
                
                if selected_indices:
                    selected_vectors = self.material_vectors[selected_indices]
                    similarities = cosine_similarity(mat_vector, selected_vectors)[0]
                    avg_similarity = float(np.mean(similarities))
                    
                    # Combine scores
                    relevance_score = (category_score + avg_similarity) / 2
                    recommendations.append((mat, relevance_score))
        
        # Sort by relevance and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_n]
    
    def optimize_pricing(self, material_id: int, 
                        lease_duration_days: int, 
                        quantity: int) -> Dict:
        """
        Calculate optimized pricing with discounts for long-term leases.
        
        Args:
            material_id: ID of the material
            lease_duration_days: Duration of lease in days
            quantity: Quantity being leased
            
        Returns:
            Dictionary with pricing details
        """
        # Find material
        material = next((mat for mat in self.materials_data if mat['id'] == material_id), None)
        
        if not material:
            return {}
        
        base_price = material.get('price_per_day', 0)
        
        # Calculate discounts
        duration_discount = 0
        if lease_duration_days >= 90:
            duration_discount = 0.20  # 20% discount for 3+ months
        elif lease_duration_days >= 30:
            duration_discount = 0.10  # 10% discount for 1+ month
        elif lease_duration_days >= 7:
            duration_discount = 0.05  # 5% discount for 1+ week
        
        quantity_discount = 0
        if quantity >= 100:
            quantity_discount = 0.15  # 15% discount for bulk
        elif quantity >= 50:
            quantity_discount = 0.10  # 10% discount
        elif quantity >= 20:
            quantity_discount = 0.05  # 5% discount
        
        # Apply discounts
        total_discount = min(duration_discount + quantity_discount, 0.30)  # Max 30% discount
        discounted_price = base_price * (1 - total_discount)
        
        total_cost = discounted_price * quantity * lease_duration_days
        
        return {
            'material_id': material_id,
            'material_name': material.get('name'),
            'base_price_per_day': base_price,
            'discounted_price_per_day': round(discounted_price, 2),
            'duration_discount_percent': round(duration_discount * 100, 1),
            'quantity_discount_percent': round(quantity_discount * 100, 1),
            'total_discount_percent': round(total_discount * 100, 1),
            'quantity': quantity,
            'lease_duration_days': lease_duration_days,
            'total_cost': round(total_cost, 2),
            'savings': round((base_price - discounted_price) * quantity * lease_duration_days, 2)
        }
