#!/bin/bash

# .githooks 디렉토리 생성
mkdir -p .githooks

# commit-msg 훅 생성 (파일이 존재하지 않을 경우에만)
if [ ! -f .githooks/commit-msg ]; then
    cat > .githooks/commit-msg << 'EOL'
#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# 커밋 메시지 패턴 정의 (예: "type: subject")
pattern="^(feat|fix|docs|style|refactor|test|chore): .{1,50}$"

if ! [[ "$commit_msg" =~ $pattern ]]; then
    echo "오류: 커밋 메시지가 지정된 규칙을 따르지 않습니다."
    echo "커밋 메시지는 다음 형식을 따라야 합니다: type: subject"
    echo "허용되는 타입: feat, fix, docs, style, refactor, test, chore, init"
    echo "제목(subject)은 50자를 넘지 않아야 합니다."
    exit 1
fi
EOL
    echo "commit-msg 훅이 생성되었습니다."
else
    echo "commit-msg 훅이 이미 존재합니다."
fi

# post-merge 훅 생성 (파일이 존재하지 않을 경우에만)
if [ ! -f .githooks/post-merge ]; then
    cat > .githooks/post-merge << 'EOL'
#!/bin/bash

# Git 설정을 변경하여 .githooks 디렉토리를 사용하도록 설정
git config core.hooksPath .githooks

# 모든 훅 파일에 실행 권한 부여
chmod +x .githooks/*

echo "Git hooks가 성공적으로 업데이트되었습니다."
echo "현재 사용 중인 hooks:"
ls -l .githooks
EOL
    echo "post-merge 훅이 생성되었습니다."
else
    echo "post-merge 훅이 이미 존재합니다."
fi

# 훅 파일들에 실행 권한 부여
chmod +x .githooks/*

echo "Git hooks 설정이 완료되었습니다."
echo ".githooks 디렉토리가 확인되었으며, commit-msg와 post-merge 훅이 추가되었습니다."
echo "이제 pull을 받을 때마다 자동으로 Git hooks가 업데이트됩니다."

# Git 설정에 대한 주의사항
echo ""
echo "주의: 이 스크립트는 로컬 Git 설정을 변경합니다."
echo "각 개발자는 이 스크립트를 한 번 실행해야 합니다."
echo "Git 설정을 변경하려면 다음 명령어를 실행하세요:"
echo "git config core.hooksPath .githooks"