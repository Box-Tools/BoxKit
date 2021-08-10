#include <string>

class World
{
public:
    World() {}
    World(std::string msg);
    virtual ~World() {}
    void set(std::string msg);
    std::string greet();

private:
    std::string msg;
};
