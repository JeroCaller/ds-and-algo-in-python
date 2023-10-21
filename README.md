# 자료구조와 알고리즘 구현 코드.

자료구조와 알고리즘을 공부하면서 배운 자료구조들 및 몇몇 알고리즘들을 
파이썬으로 직접 구현해본 모듈 모음. 


changelog
- - -

> 2023-10-21
> - tree.py의 Tree(), PathTree()에서 계층 간 구분 기호를 중간에 바꾸거나 확인할 수 있는 기능 추가 및 해당 기능 테스트 코드 추가 (테스트 성공). -> Tree().delimiter 또는 PathTree().delimiter를 이용하면 됨.

> 2023-10-20
> - tree.py의 PathTree()의 appendAbs() 메서드 추가. 
>   - 노드의 절대경로로 새 노드 삽입 기능. 
> - appendAbs() 단위 테스트, 프린트 테스트 추가. -> (모두 테스트 성공)
> - tree.py의 PathTree()의 append() 메서드 독스트링 오타 수정. 
