import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 10,        
  duration: '10s',
  thresholds: {
    http_req_duration: ['p(95) <500'],
    http_req_failed: ['rate <0.01'],
    checks: ['rate>0.99']
  }
};

export default function () {
  const res = http.get('http://web:8000/');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}