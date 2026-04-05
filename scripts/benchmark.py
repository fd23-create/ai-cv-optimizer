#!/usr/bin/env python3
"""
Benchmark script for AI CV Optimizer ML Service
Tests performance of the ML analysis pipeline
"""

import time
import json
import statistics
import requests
from pathlib import Path
from typing import List, Dict, Any
import argparse

class MLCVOptimizerBenchmark:
    """Benchmark class for ML CV Optimizer service"""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.results = []
        
    def run_benchmark(self, test_files: List[str], iterations: int = 3) -> Dict[str, Any]:
        """Run complete benchmark suite"""
        print(f"🚀 Starting benchmark with {len(test_files)} files, {iterations} iterations each")
        
        # Test health endpoint
        self._test_health_check()
        
        # Test file analysis
        for file_path in test_files:
            self._test_file_analysis(file_path, iterations)
        
        # Test skills extraction
        self._test_skills_extraction(test_files)
        
        # Test resume scoring
        self._test_resume_scoring(test_files)
        
        # Generate report
        return self._generate_report()
    
    def _test_health_check(self):
        """Test health check endpoint"""
        print("📊 Testing health check...")
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                duration = (end_time - start_time) * 1000
                self.results.append({
                    'test': 'health_check',
                    'duration_ms': duration,
                    'success': True,
                    'status_code': response.status_code
                })
                print(f"✅ Health check: {duration:.2f}ms")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Health check error: {e}")
            self.results.append({
                'test': 'health_check',
                'duration_ms': 0,
                'success': False,
                'error': str(e)
            })
    
    def _test_file_analysis(self, file_path: str, iterations: int):
        """Test complete file analysis"""
        print(f"📄 Testing file analysis: {Path(file_path).name}")
        
        durations = []
        success_count = 0
        
        for i in range(iterations):
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    start_time = time.time()
                    
                    response = requests.post(
                        f"{self.base_url}/analyze",
                        files=files,
                        timeout=60
                    )
                    
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000
                    durations.append(duration)
                    
                    if response.status_code == 200:
                        success_count += 1
                        data = response.json()
                        
                        # Validate response structure
                        self._validate_analysis_response(data)
                        
                    else:
                        print(f"❌ Analysis failed: {response.status_code}")
                        
            except Exception as e:
                print(f"❌ Analysis error: {e}")
        
        if durations:
            avg_duration = statistics.mean(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            self.results.append({
                'test': 'file_analysis',
                'file': Path(file_path).name,
                'iterations': iterations,
                'success_count': success_count,
                'avg_duration_ms': avg_duration,
                'min_duration_ms': min_duration,
                'max_duration_ms': max_duration,
                'success_rate': success_count / iterations
            })
            
            print(f"✅ File analysis: avg {avg_duration:.2f}ms, success rate {success_count}/{iterations}")
    
    def _test_skills_extraction(self, test_files: List[str]):
        """Test skills extraction endpoint"""
        print("🔍 Testing skills extraction...")
        
        durations = []
        total_skills = 0
        
        for file_path in test_files[:3]:  # Test first 3 files
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    start_time = time.time()
                    
                    response = requests.post(
                        f"{self.base_url}/extract-skills",
                        files=files,
                        timeout=30
                    )
                    
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000
                    durations.append(duration)
                    
                    if response.status_code == 200:
                        data = response.json()
                        skills = data.get('skills', [])
                        total_skills += len(skills)
                        
            except Exception as e:
                print(f"❌ Skills extraction error: {e}")
        
        if durations:
            avg_duration = statistics.mean(durations)
            self.results.append({
                'test': 'skills_extraction',
                'files_tested': len(test_files[:3]),
                'avg_duration_ms': avg_duration,
                'total_skills_extracted': total_skills,
                'avg_skills_per_file': total_skills / len(test_files[:3]) if test_files else 0
            })
            
            print(f"✅ Skills extraction: avg {avg_duration:.2f}ms, {total_skills} skills total")
    
    def _test_resume_scoring(self, test_files: List[str]):
        """Test resume scoring endpoint"""
        print("📈 Testing resume scoring...")
        
        durations = []
        scores = []
        
        for file_path in test_files[:2]:  # Test first 2 files
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    start_time = time.time()
                    
                    response = requests.post(
                        f"{self.base_url}/score-resume",
                        files=files,
                        timeout=30
                    )
                    
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000
                    durations.append(duration)
                    
                    if response.status_code == 200:
                        data = response.json()
                        score = data.get('scores', {}).get('overall', 0)
                        scores.append(score)
                        
            except Exception as e:
                print(f"❌ Resume scoring error: {e}")
        
        if durations:
            avg_duration = statistics.mean(durations)
            avg_score = statistics.mean(scores) if scores else 0
            
            self.results.append({
                'test': 'resume_scoring',
                'files_tested': len(test_files[:2]),
                'avg_duration_ms': avg_duration,
                'avg_score': avg_score,
                'scores': scores
            })
            
            print(f"✅ Resume scoring: avg {avg_duration:.2f}ms, avg score {avg_score:.1f}")
    
    def _validate_analysis_response(self, data: Dict[str, Any]):
        """Validate analysis response structure"""
        required_fields = ['success', 'analysis']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        if not data['success']:
            raise ValueError("Analysis was not successful")
        
        analysis = data['analysis']
        analysis_fields = ['overallScore', 'scores', 'skills', 'experience', 'education']
        
        for field in analysis_fields:
            if field not in analysis:
                raise ValueError(f"Missing analysis field: {field}")
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive benchmark report"""
        print("\n📊 Generating benchmark report...")
        
        report = {
            'timestamp': time.time(),
            'summary': self._generate_summary(),
            'detailed_results': self.results,
            'recommendations': self._generate_recommendations()
        }
        
        # Save report to file
        report_file = f"benchmark_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {report_file}")
        return report
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        summary = {
            'total_tests': len(self.results),
            'successful_tests': len([r for r in self.results if r.get('success', True)]),
            'performance': {}
        }
        
        # Calculate performance metrics
        for result in self.results:
            test_name = result['test']
            if test_name not in summary['performance']:
                summary['performance'][test_name] = {
                    'avg_duration_ms': 0,
                    'min_duration_ms': float('inf'),
                    'max_duration_ms': 0,
                    'samples': 0
                }
            
            perf = summary['performance'][test_name]
            
            if 'avg_duration_ms' in result:
                perf['avg_duration_ms'] += result['avg_duration_ms']
                perf['min_duration_ms'] = min(perf['min_duration_ms'], result.get('min_duration_ms', result['avg_duration_ms']))
                perf['max_duration_ms'] = max(perf['max_duration_ms'], result.get('max_duration_ms', result['avg_duration_ms']))
                perf['samples'] += 1
        
        # Calculate averages
        for test_name, perf in summary['performance'].items():
            if perf['samples'] > 0:
                perf['avg_duration_ms'] /= perf['samples']
                if perf['min_duration_ms'] == float('inf'):
                    perf['min_duration_ms'] = 0
        
        return summary
    
    def _generate_recommendations(self) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Analyze file analysis performance
        analysis_results = [r for r in self.results if r['test'] == 'file_analysis']
        if analysis_results:
            avg_duration = statistics.mean([r['avg_duration_ms'] for r in analysis_results])
            success_rate = statistics.mean([r['success_rate'] for r in analysis_results])
            
            if avg_duration > 5000:
                recommendations.append("⚠️  File analysis is slow (>5s). Consider optimizing text processing or adding caching.")
            
            if success_rate < 0.9:
                recommendations.append("❌ Low success rate in file analysis. Check error handling and input validation.")
        
        # Analyze skills extraction performance
        skills_results = [r for r in self.results if r['test'] == 'skills_extraction']
        if skills_results:
            avg_duration = statistics.mean([r['avg_duration_ms'] for r in skills_results])
            
            if avg_duration > 1000:
                recommendations.append("⚠️  Skills extraction is slow (>1s). Consider optimizing NLP models.")
        
        # General recommendations
        if len(self.results) == 0:
            recommendations.append("❌ No tests completed successfully. Check service health and connectivity.")
        else:
            recommendations.append("✅ Benchmark completed successfully. Review detailed results for optimization opportunities.")
        
        return recommendations

def find_test_files(directory: str = "./test_files") -> List[str]:
    """Find test PDF files"""
    test_dir = Path(directory)
    
    if not test_dir.exists():
        print(f"❌ Test directory not found: {directory}")
        return []
    
    # Look for PDF files
    pdf_files = list(test_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {directory}")
        return []
    
    print(f"📁 Found {len(pdf_files)} test files")
    return [str(f) for f in pdf_files]

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Benchmark ML CV Optimizer service")
    parser.add_argument("--url", default="http://localhost:5001", help="Base URL of ML service")
    parser.add_argument("--dir", default="./test_files", help="Directory containing test files")
    parser.add_argument("--iterations", type=int, default=3, help="Number of iterations per test")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Find test files
    test_files = find_test_files(args.dir)
    if not test_files:
        return 1
    
    # Run benchmark
    benchmark = MLCVOptimizerBenchmark(args.url)
    report = benchmark.run_benchmark(test_files, args.iterations)
    
    # Print summary
    print("\n" + "="*50)
    print("BENCHMARK SUMMARY")
    print("="*50)
    print(f"Total tests: {report['summary']['total_tests']}")
    print(f"Successful tests: {report['summary']['successful_tests']}")
    
    print("\nPerformance:")
    for test_name, perf in report['summary']['performance'].items():
        print(f"  {test_name}:")
        print(f"    Average duration: {perf['avg_duration_ms']:.2f}ms")
        print(f"    Min duration: {perf['min_duration_ms']:.2f}ms")
        print(f"    Max duration: {perf['max_duration_ms']:.2f}ms")
        print(f"    Samples: {perf['samples']}")
    
    print("\nRecommendations:")
    for rec in report['recommendations']:
        print(rec)
    
    return 0

if __name__ == "__main__":
    exit(main())
