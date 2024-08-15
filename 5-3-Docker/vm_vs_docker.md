### docker 과 가상머신의 차이
- 가상머신은 hypervisor 위에 guest os가 올라간다. 
- docker은 리눅스 커널에서 제공하는 cgroups, namespaces를 활용해 각각의 컨테이너가 모두 host os(linux)의 커널을 사용하는 게 가능하게 합니다.

### docker의 장점
- guest os가 있어야하는 가상머신에 비해 docker는 가볍고, 메모리 사용량도 낮으며, 가동과 중단이 더 빠릅니다.
- docker 자체에서 container들간 통신을 편리하게 할 수 있도록 지원합니다. 
- 이미 it업계의 표준처럼 자리잡아서 자료들이 많습니다.



