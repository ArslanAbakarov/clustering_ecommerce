import os
from shiny import App, ui, reactive, render
import pandas as pd
from pycaret.classification import load_model
import numpy as np
import pickle  # For loading the model
# from pycaret.clustering import *
import random

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

file = 'models/kmeans_customers_model'

# from pycaret.clustering import predict_model

# Load the model using PyCaret's load_model
# kmeans = load_model('models/kmeans_model')
# kmeans = load_model('models/kmeans_model_customers_model')

with open(file, 'rb') as file:
    kmeans = pickle.load(file)

# kmeans = pickle.load(file)

df = pd.read_csv("dataset/ecommerce_20k.csv")

# With Aggregation
product_features = df.groupby(['user_id', 'product_name']).agg(
    purchase_count=('order_id', 'count'),
    reorder_rate=('reordered', 'mean'),
    avg_days_between=('days_since_prior_order', 'mean'),
    avg_cart_position=('add_to_cart_order', 'mean')
).reset_index()

# Customer product matrix
customer_product_matrix = product_features.pivot(
    index='user_id',
    columns='product_name',
    values='purchase_count'
).fillna(0)

# customer_product_matrix['Cluster'] = kmeans.fit_predict(customer_product_matrix)
customer_clusters = kmeans.predict(customer_product_matrix)
customer_product_matrix['Cluster'] = customer_clusters

cluster_product_preferences = customer_product_matrix.groupby('Cluster').mean()

firstName = ['Sean', 'John', 'George', 'Michael'] 
lastName = ['Grogg', 'Smith', 'Washington', 'Jackson', 'Daniels'] 

users_arr = ["152060", "44755", "169119", "162421"]
user_name = ""
users_logins = []

# Association Rules for Cluster 0:
#            antecedents                   consequents   support  confidence  \
# 0  (baby food formula)                (fresh fruits)  0.022829    0.735471   
# 1  (baby food formula)            (fresh vegetables)  0.016808    0.541483   
# 2  (baby food formula)             (packaged cheese)  0.005997    0.193186   
# 3  (baby food formula)  (packaged vegetables fruits)  0.008559    0.275752   
# 4  (baby food formula)                      (yogurt)  0.007664    0.246894   


# Association Rules for Cluster 1:
#   antecedents                   consequents   support  confidence      lift
# 0     (bread)                        (milk)  0.006566    0.106949  1.098158
# 1     (bread)             (packaged cheese)  0.007257    0.118207  1.250789
# 2     (bread)  (packaged vegetables fruits)  0.008305    0.135287  0.972958
# 3     (bread)                      (yogurt)  0.007912    0.128882  1.052540
# 4    (cereal)                        (milk)  0.005183    0.121474  1.247309

cluster0_rules['baby food formula'] = ['fresh fruits', 'fresh vegetables', 'packaged cheese', 'packaged vegetables fruits', 'yogurt']
cluster1_rules['bread'] = ['milk', 'packaged cheese', 'packaged vegetables fruits', 'yogurt']
cluster1_rules['cereal'] = ['milk']

cluster_rules[0] = cluster0_rules
cluster_rules[1] = cluster1_rules


for user_id in users_arr:
    users_logins.append(random.choice(firstName) + " " + random.choice(firstName) + " - " + user_id)

# Define the UI
app_ui = ui.page_fluid(
    
    ui.HTML("""
        <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/amazon-ember">
        <!--<script type="text/javascript" src="/js/scripts.js"></script>-->

        <script>        
        function AddToCartClick(sender) {
            // alert("Added")
            sender.outerHTML = '<div class="added-item-button">In cart</div>';
            return 0;
        }
        </script>
    """),
    
    ui.tags.style("""
                
        body {
            background-color: rgb(227, 230, 230);
            color: black;
            # padding-top: 20px;
        }
        
        .container {
            background-color: white !important;
            color: black;
            padding: 20px;
         
        }
        
        .container-fluid {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        .inspired-section {
            margin-top: 40px;
            background-color: white;
            display: block;
            overflow:auto; 
        }
        
        
        .product-image {
            text-align: center;
        }
        
        .product-image img {
            
            width: 200px;    /* Desired width */
            height: 150px;   /* Desired height */
            object-fit: cover;
            overflow: hidden;
        }
        
        .product-name {
            font-size: 18px;
            font-weight: 400;
            display: inline-block;
            line-height: 22px;
            margin-top: 12px;
        }
        
        .price-label {
            font-size: 21px;
            font-weight: 500;
            position: relative;
        }
        
        .price-number {
            float: left;
            font-size: 34px;
            line-height: 34px;
        }
        
        .dollar-sign {
            font-size: 15px;
            float: left;
        }
        
        .decimals {
            font-size: 15px;
        }
        
        .introduction {
            margin-top: 20px;
        }
        
        .recommended-product {
            display: block;
            float: left;
            background-color: rgb(227, 230, 230);
            padding: 20px;
            
            margin: 10px;
            min-height: 220px;
            width: auto;
            min-width: 160px;
        }
        
        ul {
            list-style-type: none;
            padding: 0;
        }
        
        .upper-bar {
            width: 100%;
            height: 60px;
            background-color: rgb(15,17,17);
            color: white;
        }
        
        .shipping-line {
            display: block;
            width: 100%;
            clear: both;
            margin-top: 10px;
        }
        
        .delivery-line {
            display: block;
            width: 100%;
            clear: both;
            margin-top: 10px;
        }
        
        .add-to-cart {
            display: block;
            width: 100%;
            clear: both;
            margin-top: 10px;
            background-color: rgb(255,216,20);
            color: black;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            border-radius: 15px;
            font-weight: 500;
        }
        
        .added-item-button {
            font-weight: 800;
        }
        
    """),
      
    ui.tags.head(
        # Link to a Bootswatch theme (Cerulean)
        # ui.tags.link(rel="stylesheet", href="css/bootstrap.css")
        
        # ui.tags.link(
        #     rel="stylesheet",
        #     href="css/custom.css"
        # ),
    ),
    
    # https://shiny.posit.co/py/api/core/ui.input_slider.html
    
    ui.div(
        
        ui.div(
          ui.div(
              ui.HTML(user_name),
         ),
          class_="upper-bar"  
        ),
        
        # ui.div(
        #     # ui.output_image("logoimage"),
        #     class_="container",
        # ),
        
        # output hr
        
        # ui.hr(),
        
        ui.div(
            ui.h1("Select your user Profile"),            
            class_="container introduction",
        ),
    
        ui.div(
            
            ui.div(
                    # ui.p("The model was developed using PyCaret’s classification module, which automates many of the preprocessing, model selection, and tuning steps. Various algorithms were tested, and the best-performing model was selected based on evaluation metrics such as accuracy, precision, recall, and F1-score. The final model is designed to predict whether an individual has diabetes (binary classification: Yes/No) based on the input features."),
                    class_="",
            ),
            
            ui.div (        
                    
                # ui.h2("Please fill in the form:"),
                # Input fields for model features
                # ui.input_slider("bmi", "BMI", 0.0, 100.0, value=3.029167),
        
                # https://shiny.posit.co/py/api/core/ui.input_select.html
                ui.input_select("user_id", "User", users_logins, selected="No"),

                # Button to trigger prediction
                ui.input_action_button("predict", "Recommend"),

                # Output the prediction
                # ui.output_text_verbatim("prediction"),
                ui.output_ui("prediction"),  
                class_="parameters-container",
                
            ),
            
            class_="container",
        ),
        class_="page-container",
    )
)

# Define the server logic
def server(input, output, session):
    
    logoimg: dict = {
        "src": "sig-blk-en.svg",
        "height": "40px",
        "content_type": "image/svg+xml"  # Specify the type of the image, especially for SVG
    }
    
    # load dataset from csv
    
    # Define the prediction logic
    @output
    
    @render.image
    def logoimage():
        # from pathlib import Path
        return logoimg

    
    @render.text
    def prediction():
        
        # Wait until the button is clicked
        if input.predict() == 0:
            return "Click 'Predict' to get the result."

        # predicted users cluster
        print(input.user_id())
        
        # get substring after dash
        target_user_id = input.user_id().split(" - ")[1]        
        target_user_id = int(target_user_id)
        
        user_data = customer_product_matrix.loc[target_user_id]
        
        cluster_number = user_data['Cluster']
        
        print("Cluster: " + str(user_data['Cluster']))
        
        top_products_per_cluster = {}
        for cluster in cluster_product_preferences.index:
            top_products = cluster_product_preferences.loc[cluster].nlargest(16)  # Top 5 products
            top_products_per_cluster[cluster] = top_products.index.tolist()

        # Print or view top products per cluster
        for cluster, products in top_products_per_cluster.items():
            print(f"Top products for Cluster {cluster}: {products}")        
        
        top_products_per_cluster = top_products_per_cluster[cluster_number]
        
        recommended_html = ""
        
        delivery_lines = ["Get it <b>Tomorrow</b>", "Today by 10:00 PM"]
        shipment = ["FREE Shipping", "FREE One-Day", "$19.99 shipping"]
                
        delivery_line = random.choice(delivery_lines)
        
        recommended = top_products_per_cluster
      
        counter = 0
        for product_name in recommended:
            
            random_price = np.random.randint(10, 50)
            random_decimals = np.random.randint(10, 99)
            image_path = "images/" + product_name + ".jpg"
            # check if image exists
            relative_path = os.path.join(os.path.dirname(__file__), "www", image_path)
            if not os.path.exists(relative_path):
                image_path = "images/basket.jpg"
                
            if counter == 0:
                recommended_html += "<div class='row'>"
                
            recommended_html += f"""
            <li class="col">
                
                    <div class="recommended-product">
                        <div class="product-image"><img src="{image_path}"/></div>
                        <div class="product-name">{product_name}</div>
                        <div class="price-label">
                            <div class="dollar-sign">$</div>
                            <div class="price-number">{random_price}</div>
                            <div class="decimals">{random_decimals}</div>
                        </div>
                        <div class="shipping-line">{random.choice(shipment)}</div>
                        <div class="delivery-line">{delivery_line}</div>
                        <button  onclick="AddToCartClick(this)" class="add-to-cart">Add to Cart</button>
                    </div>
                
            </li>
            """
     
            counter += 1
                   
            # if counter == 4:
            #     recommended_html += "</div>"
            #     counter = 0
                
        recommended_html += "</div>"
        
        inspired_html = f"""
        <div class="inspired-section container">
            <div>
                <h2>Inspired by your shopping trends</h2>
                <ul>
                    {recommended_html} 
                </ul>
            </div>
        </div>"""
        
        return ui.HTML(inspired_html);

        
        # if input.gender() == "Male":
        #     genderFemale = 0
        #     genderMale = 1
        #     genderOther = 0        
        
        # # Create a DataFrame with all required features, including one-hot encoded categories
        # features = pd.DataFrame({
        #     'age': [input.age()],
        #     'hypertension': [hypertension],  # Placeholder, add input fields for these if needed
        #     'heart_disease': [heart_disease],
        #     'bmi': [input.bmi()],
        #     'HbA1c_level': [input.HbA1c_level()],  # Placeholder value
        #     'blood_glucose_level': [input.blood_glucose_level()],  # Placeholder value
            
        # })

        # Make prediction using the pre-trained model
        # trained_model = model.steps[-1][1]
        # predicted_class = model.predict(features)[0]
        
        # Return the predicted class
        # return f'Predicted Diabetes: {"At risk of developing diabetes." if predicted_class == 1 else "Not at risk of developing diabetes. Good job."} '
        
        # if predicted_class == 1:
        #     return ui.HTML('<br><div class="prediction-label" style="color: red">Predicted: At risk of developing diabetes.</div>')
        # else:
        #     return ui.HTML('<br><div class="prediction-label" style="color:green">Predicted: Not at risk of developing diabetes. <br></div>')
        # return f'Predicted Diabetes: {"At risk of developing diabetes." if predicted_class == 1 else "Not at risk of developing diabetes. Good job."} '
    

# Create the app object
app = App(app_ui, server, static_assets=os.path.join(os.path.dirname(__file__), "www") )