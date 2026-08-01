"""
Model evaluation module - Fixed with directory creation
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix
)
from pathlib import Path

def evaluate_models(model_dir='models/', test_data_path='outputs/metrics/'):
    """
    Evaluate all saved models on the test set and generate comparison.
    """
    # Create required directories
    Path('outputs/plots').mkdir(parents=True, exist_ok=True)
    Path('outputs/metrics').mkdir(parents=True, exist_ok=True)
    print("✅ Directories created/verified")
    
    # Load test data
    X_test = pd.read_csv(f"{test_data_path}/X_test.csv")
    y_test = pd.read_csv(f"{test_data_path}/y_test.csv").values.ravel()

    # List models
    model_files = Path(model_dir).glob('*.pkl')
    results = []
    
    # Create figure for confusion matrices
    model_list = list(model_files)
    n_models = len(model_list)
    fig, axes = plt.subplots(1, n_models, figsize=(5*n_models, 5))
    if n_models == 1:
        axes = [axes]

    for idx, model_path in enumerate(model_list):
        model_name = model_path.stem
        pipeline = joblib.load(model_path)

        # Predict
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, 'predict_proba') else None

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_proba) if y_proba is not None else np.nan

        results.append({
            'Model': model_name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1': f1,
            'ROC_AUC': roc_auc
        })

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
        axes[idx].set_title(f'{model_name}\nConfusion Matrix')
        axes[idx].set_xlabel('Predicted')
        axes[idx].set_ylabel('Actual')

    plt.tight_layout()
    plt.savefig('outputs/plots/confusion_matrices.png')
    plt.close()

    # Save metrics table
    results_df = pd.DataFrame(results)
    results_df.to_csv('outputs/metrics/model_comparison.csv', index=False)
    print("✅ Model comparison saved")

    # Feature importance for Random Forest (if exists)
    rf_path = Path(model_dir) / 'RandomForest.pkl'
    if rf_path.exists():
        try:
            pipeline = joblib.load(rf_path)
            preprocessor = pipeline.named_steps['preprocessor']
            cat_cols = preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(
                preprocessor.transformers_[1][2]
            )
            all_features = preprocessor.transformers_[0][2] + list(cat_cols)
            importances = pipeline.named_steps['classifier'].feature_importances_
            imp_df = pd.DataFrame({'Feature': all_features, 'Importance': importances})
            imp_df = imp_df.sort_values('Importance', ascending=False)
            
            plt.figure(figsize=(10, 6))
            sns.barplot(data=imp_df.head(15), x='Importance', y='Feature')
            plt.title('Random Forest Feature Importances')
            plt.tight_layout()
            plt.savefig('outputs/plots/feature_importance.png')
            plt.close()
            imp_df.to_csv('outputs/metrics/feature_importances.csv', index=False)
            print("✅ Feature importance plot saved")
        except Exception as e:
            print(f"⚠️  Could not generate feature importance: {e}")

    print("✅ Evaluation complete. Check outputs/metrics/ and outputs/plots/")

if __name__ == '__main__':
    evaluate_models()