import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    models: {
      ann: {
        name: 'Artificial Neural Network',
        type: 'deep_learning',
        accuracy: '97.19%',
        description: 'Mạng neural nhân tạo với regularization'
      },
      random_forest: {
        name: 'Random Forest',
        type: 'ensemble',
        accuracy: '97.39%',
        description: 'Ensemble của các decision trees'
      },
      xgboost: {
        name: 'XGBoost',
        type: 'gradient_boosting',
        accuracy: '97.47%',
        description: 'Gradient boosting tối ưu hóa'
      },
      knn: {
        name: 'K-Nearest Neighbors',
        type: 'instance_based',
        accuracy: '97.46%',
        description: 'Thuật toán dựa trên khoảng cách'
      },
      meta: {
        name: 'Meta Model',
        type: 'meta_learning',
        accuracy: '97.61%',
        description: 'Linear Regression kết hợp các mô hình cơ sở'
      }
    },
    classes: [
      'Thịt loại 1',
      'Thịt loại 2', 
      'Thịt loại 3',
      'Thịt loại 4',
      'Thịt hỏng'
    ],
    ensemble_method: 'meta_learning'
  })
}
