#include <cbox/library.h>
#include <string.h>
/*
 *
 *
 */
namespace cbox::library {
Monitor::Monitor(const char *type) : max_progress(0), progress(0) {
  this->type = type;

  if (strcmp(this->type, "action") == 0) {
    this->bar->set_option(indicators::option::Start{"["});
    this->bar->set_option(indicators::option::Fill{"■"});
    this->bar->set_option(indicators::option::Lead{"■"});
    this->bar->set_option(indicators::option::Remainder{"-"});
    this->bar->set_option(indicators::option::End{"]"});
    this->bar->set_option(indicators::option::ShowPercentage{true});
    this->bar->set_option(
        indicators::option::ForegroundColor{indicators::Color::cyan});
    this->bar->set_option(indicators::option::BarWidth{50});
    this->bar->set_option(indicators::option::FontStyles{
        std::vector<indicators::FontStyle>{indicators::FontStyle::bold}});

  } else if (strcmp(this->type, "test") == 0) {
    this->bar->set_option(indicators::option::BarWidth{0});
    this->bar->set_option(indicators::option::Start{""});
    this->bar->set_option(indicators::option::Fill{""});
    this->bar->set_option(indicators::option::Lead{""});
    this->bar->set_option(indicators::option::Remainder{""});
    this->bar->set_option(indicators::option::End{""});
    this->bar->set_option(
        indicators::option::ForegroundColor{indicators::Color::green});
    this->bar->set_option(indicators::option::ShowPercentage{true});
    this->bar->set_option(indicators::option::FontStyles{
        std::vector<indicators::FontStyle>{indicators::FontStyle::bold}});
  }
}

void Monitor::setlimit(int iterlimit) {
  this->max_progress = iterlimit;
  this->bar->set_option(indicators::option::MaxProgress{this->max_progress});
  this->spinner->set_option(
      indicators::option::MaxProgress{this->max_progress});
}

void Monitor::update(std::string msg, int progress) {
  if (strcmp(this->type, "action") == 0 || strcmp(this->type, "test") == 0) {
    ++this->progress;
    this->bar->set_option(indicators::option::PrefixText{msg});
    this->bar->tick();
  }
}

const char *Monitor::gettype() { return this->type; }
/*
 */
} // namespace cbox::library
