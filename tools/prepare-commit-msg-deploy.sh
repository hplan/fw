#!/bin/bash

cat << EOF > ./repo/hooks/prepare-commit-msg
#!/bin/bash
#
# An example hook script to prepare the commit log message.
# Called by "git commit" with the name of the file that has the
# commit message, followed by the description of the commit
# message's source.  The hook's purpose is to edit the commit
# message file.  If the hook fails with a non-zero status,
# the commit is aborted.
#
# To enable this hook, rename this file to "prepare-commit-msg".

# This hook includes three examples.  The first comments out the
# "Conflicts:" part of a merge commit.
#
# The second includes the output of "git diff --name-status -r"
# into the message, just before the "git status" output.  It is
# commented because it doesn't cope with --amend or with squashed
# commits.
#
# The third example adds a Signed-off-by line to the message, that can
# still be edited.  This is rarely a good idea.

addMsg() {
    # Get name of current branch
    BRANCH_NAME=\$(git symbolic-ref --short -q HEAD)

    # First blank line is title, second is break for body, third is start of body
    BODY=\`cut -d \| -f 6 \$1 | grep -v -E .\+ -n | cut -d ':' -f1 | sed '3q;d'\`

    # Put in string "(branch_name/): " at start of commit message body.
    # For templates with commit bodies
    if test ! -z \$BODY; then
        awk 'NR=='\$BODY'{\$0="\('\$NAME'/\): "}1;' \$1 > tmp_msg && mv tmp_msg "\$1"
    else
        sed -i "1i[NBF/INTERNAL/Bug]" \$1 
        sed -i "2i\\\\" \$1
        sed -i "3iCause: None" \$1
        sed -i "4iSolution: None" \$1
        sed -i "5iFixed Version: \`date "+%Y.%m.%d"\`" \$1
        sed -i "6iBranch: \$BRANCH_NAME" \$1
    fi
}


# You might need to consider squashes
case "\$2,\$3" in
    # Commits that already have a message
    commit,?*)
    ## git commit --amend
    ;;

    # Messages are one line messages you decide how to handle
    message,)
        ## git commit -m "msg"
        BRANCH_NAME=\$(git symbolic-ref --short -q HEAD)
        echo "[INTERNAL] \`cat \$1\`" > \$1
        echo "" >> \$1
        echo "Cause: None" >> \$1
        echo "Solution: None" >> \$1
        echo "Fixed Version: \`date "+%Y.%m.%d"\`" >> \$1
        echo "Branch: \$BRANCH_NAME" >> \$1
    ;;

    # Merge commits
    merge,)
    # Comments out the "Conflicts:" part of a merge commit.
        perl -i.bak -ne 's/^/# /, s/^# #/#/ if /^Conflicts/ .. /#/; print' "\$1"
    ;;

    # Non-merges with no prior messages
    *)
        addMsg \$1
    ;;
esac
EOF

chmod +x ./repo/hooks/prepare-commit-msg

git config --global --unset commit.template > /dev/null

PCM_PATT="`pwd`/repo/hooks/prepare-commit-msg"

hook_dirs=`find -name hooks`
for d in $hook_dirs; do
   cd $d
   if [ "./repo/hooks" == "$d" ]; then
       cd - > /dev/null
       continue
   fi
   sudo ln -sf $PCM_PATT . 
   cd - > /dev/null
done

echo "done"
