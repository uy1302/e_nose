import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    sensor_features: ['MQ136', 'MQ137', 'TEMP', 'HUMI'],
    sensor_count: 4,
    sensor_types: {
      gas_sensors: ['MQ136', 'MQ137'],
      environmental_sensors: ['TEMP', 'HUMI']
    },
    sensor_descriptions: {
      'MQ136': 'Cảm biến khí đa năng',
      'MQ137': 'Cảm biến khí ammonia',
      'TEMP': 'Nhiệt độ (°C)',
      'HUMI': 'Độ ẩm (%)'
    }
  })
}
