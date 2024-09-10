#!/bin/bash

# .githooks 디렉토리 생성
mkdir -p .githooks

# commit-msg 훅 생성
cat > .githooks/commit-msg << 'EOL'
#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# 커밋 메시지 패턴 정의 (예: "type: subject")
pattern="^(feat|fix|docs|style|refactor|test|chore): .{1,50}$"

if ! [[ "$commit_msg" =~ $pattern ]]; then
    echo "오류: 커밋 메시지가 지정된 규칙을 따르지 않습니다."
    echo "커밋 메시지는 다음 형식을 따라야 합니다: type: subject"
    echo "허용되는 타입: feat, fix, docs, style, refactor, test, chore"
    echo "제목(subject)은 50자를 넘지 않아야 합니다."
    exit 1
fi
EOL

# post-merge 훅 생성
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

# 훅 파일들에 실행 권한 부여 및 Git 설정
chmod +x .githooks/*
git config core.hooksPath .githooks

echo "Git hooks가 성공적으로 설정되었습니다."
echo ".githooks 디렉토리가 생성되었으며, commit-msg와 post-merge 훅이 추가되었습니다."
echo "이제 pull을 받을 때마다 자동으로 Git hooks가 업데이트됩니다."