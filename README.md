# Chez
Guess their menu

[] : menu name
() : food name
n..m : number range

**확실한 단서만 주는 규칙** -> superset
**확실한 단서를 주는 규칙** -> set

여기서 확실한 단서란 제공된 단서의 경우의 수가 하나로 고정되는 경우를 뜻함

고정, 제거, 또 뭐가 있을까요

일단 확실한 것들 전부 적어놓으면 남는 게 생길테니 그 때 다시 생각해봅시다

관계를 나타내는 규칙들도 따로 명시해주시면 될 것 같아요 => relation
이런 규칙들이 set 특징을 가지지 않는 모든 규칙인지 확인해봐야 할 것 같아요

# 관계가 정의하기 되게 애매하네요 [위치적 관계(ex. 이웃, left/right, edge), 메뉴적 관계(ex. a를 시킨 사람은 b를 시키지 않았다)]
    1. 이웃이 ()를 원한다
    2. (a)를 시킨 사람은 (b)를 시킨 사람 옆에 있다
    3. (a)를 시킨 사람은 다른 []를 원한다 / [A(a)]를 시킨 사람은 동일한 [B(b)]를 원한다. 그리고 [C(c)]를 원하지 않는다
    4. edge에 앉은 사람은 ()를 원한다
    5. ()를 원하는 두 명은 서로 옆에 앉아있다.
    6. (left/right) 저쪽에 있는 모두는 같은 []를 원한다

1. I don't want (). <!-- 자신 1 음식 제거 --> # superset
2. Nobody wants (), or (). <!-- 모든 인원 2 음식 제거 --> # superset
3. My neighbors both want the same (). <!-- 양 옆 사람 동일 음식  --> # relation
4. Everbody else wants (). <!-- 자기 자신 제외 모두 1 음식 고정 --> # superset
5. I'm the only one who wants (). <!-- 자신만 이 음식을 원함, 나머지는 싫어함 --> # superset 

6. Everybody over there wants (). (left or right)   <!-- 최소 1 명, 최대 5명의 메뉴 고정 --> # superset
7. The only one who wants () is over there. (left or right) <!--  -->   # 
8. One of my neighbors and I want (). <!-- 옆 사람 중 1 명과 자신의 음식 고정 --> # set / relation
9. The person who wants () is not sitting next to the one who wants (). <!--  --> # relation
10. Nobody wants the same [] as his neighbor. <!-- --> # relation

11. All the ones who want () want a different []. <!-- --> # relation
12. The two who want () are sitting next to each other, so are the two who want a (). <!-- --> # relation
13. One of them is the only one who wants (), and the other one is the only one who wants (). (left or right) <!-- --> 
14. My neighbor and I are the only ones who want (). <!-- --> # set / relation
15. Two of us want (). I'm the only one who wants (). <!-- --> # set 

16. I want (), but the others both want (). <!-- --> # set
17. I want (), but I don't want any (). <!-- --> # set
18. All the ones who want () also want (). None of them wants (). <!-- --> # relation
19. I want (). The other two who also want some, are sitting next to each other. <!-- --> # relation
20. Three of us want (). But I'm the only one who wants (). <!-- -->

21. The three () were ordered over there. (left or right) <!-- --> # relation
22. Two of us want () with their (), but I don't. <!-- -->
23. I'm not one of the four who wants (). No one who wants () wants (). <- diff nemu type <!-- --> # relation
24. I'm not part of the four who want (). <!-- -->
25. One of my neighbors wants (), so does one of their neighbors and another person. <!--  --> 

26. Everybody over there wants (), everybody over there wants (). They are all crazy. (left or right, and right or left) <!-- --> # set
27. The two sitting next to each other want (). <!-- --> # relation
28. My two neighbors don't want the same [] as everybody. <!-- --> # relation
29. Everybody over there wants the same [], but nobody wants (). (left or right)<!-- --> # relation
30. Two of my neighbors want (), but nobody wants a (). <!-- -->    # set

31. The two person sitting at each edge of the table want (). And someone else also want some. <!-- --> # set / relation
32. Two neighbors want the same []. They don't want any (). <!-- 여기서 neighbors는 My neighbor가 아니므로 자신을 제외한 모든 사람 포함가능 --> # relation
 



# 규칙들에서 찾아볼 수 있는 공통된 규칙들 목록

1. I want ()
2. I don't want ()
<!-- I'm the only one who wants a () = 1, 3 -->
3. Everybody else wants ()
4. 1..2 of my neighbors want ()
5. Everybody over left wants ()

6. Everybody over right wants ()
7. The only one who wants () is over left
8. The only one who wants () is over right
9. Nobody wants the same [] as his neighbor
10. All the ones who want () want a different []

11. The 2.. who want () are sitting next to each other
<!-- One of them is the only one who wants (), and the other one is the only one who wants (). (left or right) = 7, 8-->
12. My neighbor and I are the only ones who want ()
13. 1.. of us without me want ()
14. All the ones who want () also want (), None of them wants ()
<!-- I want (). The other two who also want some, are sitting next to each other. = 1, 11 -->
<!-- Three of us want (). But I'm the only one who wants (). = 13, 1, 3-->
15. The 1.. () were ordered over left.

16. The 1.. () were ordered over right.
17. 1.. of us want ()
18. No one who wants () wants (). <- diff menu type
19. One of neighbors of my neighbors want ()
20. The 2.. sitting next to each other want ()

21. My two neighbors don't want the same [] as everybody.
22. Everybody over left wants the same []
23. Everybody over right wants the same []
24. Nobody wants ()
<!-- Two of my neighbors want (), but nobody wants a (). = 4, 24 -->
25. The two person sitting at each edge of the table want ()

26. 1.. of us want same []
27. My neighbors both want the same []
28. The person who wants () is not sitting next to the one who wants a ().


# 규칙들 정리

1. setting target

- I
- Everybody
- Everybody else
- Neighbors
- Everybody over left
- Everybody over right
- The two person sitting at each edge of the table

- All the ones who want ()

2. setting spetific

    1. every
    - want ()
    - don't want ()
    
    2. 