#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask 앱이 Render.com의 PORT 환경 변수를 사용하도록 수정
"""
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('flask_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 기존 main 블록 찾기
old_main = '''if __name__ == '__main__':
    print('Flask Server Starting on port 5001...')
    print('Access from this PC: http://localhost:5001')
    print('Access from network: http://<your-ip>:5001')
    print('Viewer mode: http://localhost:5001/?mode=viewer')
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)'''

# Render.com 호환 버전
new_main = '''if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'False') == 'True'
    
    print(f'Flask Server Starting on port {port}...')
    if port == 5001:
        print('Access from this PC: http://localhost:5001')
        print('Access from network: http://<your-ip>:5001')
        print('Viewer mode: http://localhost:5001/?mode=viewer')
    
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)'''

content = content.replace(old_main, new_main)

with open('flask_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Flask 앱을 Render.com 호환으로 수정!")
print("\n변경사항:")
print("  - PORT 환경 변수 사용 (클라우드 배포용)")
print("  - DEBUG 환경 변수 지원")
print("  - 로컬(5001)과 클라우드 모두 작동")
