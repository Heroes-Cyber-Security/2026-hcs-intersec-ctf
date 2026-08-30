# HCS INTERNAL SELECTION 2026

## Challenge Folder Structure

```
<name>
├── source/
├── release/
├── poc/
└── README.md
```

| convention | explaination                                                    |
| ---------- | --------------------------------------------------------------- |
| \<name>    | name of the challenge                                           |
| source     | original code of the challenge                                  |
| release    | attachment that will be provided to the participants (optional) |
| poc        | explanation how to solve the challenge                          |
| README.md  | detail information of the challenge                             |

## Notice

### README.md convention

```md
# <name>

## Author

(your hacker name)

## Difficulty

Easy/Medium/Hard

## Description

lorem ipsum dolor sit amet

## Flag

HCS{.*}
```

### docker-compose.yaml convention

For `docker-compose.yaml` file please attach the `name` field on the configuration to prevent the orphan container, ex:

```yaml
name: this-is-challenge-name

...
```
