from flask import Flask, request, jsonify
from model import Shipment, SimulationData, MeansEndAgent, RankingAlgorithm, generate_route_report, advanced_simulation, elaborate_report, QuantumAnnealingRouteOptimizer, fuzzy_logic_ranking, deep_route_predictor, predict_route_quality, compute_sustainability_index, compute_resilience_factor, logistics_innovation_score
import random
import math
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    sim = SimulationData()
    routes = sim.simulate_multiple_routes(origin, destination, count=10)
    reports = [generate_route_report(route) for route in routes]
    return jsonify({'routes': reports})

@app.route('/shipment', methods=['POST'])
def shipment_input():
    data = request.json
    shipment = Shipment(data.get('shipment_id'), data.get('origin'), data.get('destination'), data.get('weight'), data.get('volume'), data.get('cargo_type'), datetime.strptime(data.get('shipping_date'), '%Y-%m-%d'))
    risk = shipment.calculate_risk_factor()
    return jsonify({'shipment_id': shipment.shipment_id, 'risk_factor': risk})

@app.route('/assemble', methods=['POST'])
def assemble_route():
    data = request.json
    shipment = Shipment(data.get('shipment_id'), data.get('origin'), data.get('destination'), data.get('weight'), data.get('volume'), data.get('cargo_type'), datetime.strptime(data.get('shipping_date'), '%Y-%m-%d'))
    sim = SimulationData()
    agent = MeansEndAgent()
    evaluated = agent.plan_route(shipment, sim)
    best_route, best_score = evaluated[0]
    report = generate_route_report(best_route)
    report['score'] = best_score
    return jsonify({'best_route': report})

@app.route('/rank', methods=['POST'])
def rank_routes():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    sim = SimulationData()
    routes = sim.simulate_multiple_routes(origin, destination, count=10)
    ranking_algo = RankingAlgorithm()
    ranked = ranking_algo.rank_routes(routes)
    ranked_reports = []
    for route, score in ranked:
        rep = generate_route_report(route)
        rep['score'] = score
        ranked_reports.append(rep)
    return jsonify({'ranked_routes': ranked_reports})

@app.route('/stats', methods=['GET'])
def statistics():
    routes_collection = []
    sim = SimulationData()
    for i in range(10):
        shipment = Shipment(i, random.choice(sim.locations), random.choice(sim.locations), random.uniform(50, 1500), random.uniform(10, 500), random.choice(['fragile', 'non-fragile', 'hazardous']), datetime.now() + timedelta(days=random.randint(1, 30)))
        agent = MeansEndAgent()
        evaluated = agent.plan_route(shipment, sim)
        routes_collection.append((shipment, evaluated))
    all_scores = []
    for shipment, routes in routes_collection:
        for route, score in routes:
            all_scores.append(score)
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    return jsonify({'average_score': avg_score})

@app.route('/quantum_analysis', methods=['POST'])
def quantum_analysis():
    data = request.json
    shipment = Shipment(data.get('shipment_id'), data.get('origin'), data.get('destination'), data.get('weight'), data.get('volume'), data.get('cargo_type'), datetime.strptime(data.get('shipping_date'), '%Y-%m-%d'))
    sim = SimulationData()
    routes = advanced_simulation(sim, shipment.origin, shipment.destination, count=10)
    optimizer = QuantumAnnealingRouteOptimizer(iterations=100)
    best_route, best_score = optimizer.optimize(routes)
    report = elaborate_report(best_route, shipment)
    return jsonify({'quantum_report': report})

@app.route('/fuzzy_logic_ranking', methods=['POST'])
def fuzzy_logic_ranking_endpoint():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    sim = SimulationData()
    routes = sim.simulate_multiple_routes(origin, destination, count=10)
    ranked = fuzzy_logic_ranking(routes)
    reports = []
    for route, score in ranked:
        rep = generate_route_report(route)
        rep['fuzzy_score'] = score
        reports.append(rep)
    return jsonify({'fuzzy_ranked_routes': reports})

@app.route('/ml_predict', methods=['POST'])
def ml_predict():
    data = request.json
    features = data.get('features')
    features_arr = np.array(features)
    prediction = deep_route_predictor(features_arr)
    return jsonify({'ml_prediction': float(prediction)})

@app.route('/quality', methods=['POST'])
def quality():
    data = request.json
    sim = SimulationData()
    route = sim.simulate_route(data.get('origin'), data.get('destination'))
    quality_val = predict_route_quality(route)
    return jsonify({'predicted_quality': quality_val})

if __name__ == '__main__':
    app.run(debug=True)
