require 'rake'
require 'docker'
require 'yaml'
require 'fileutils'

task :default => [:build]

def load_configuration
  YAML::load_file(File.join(File.dirname(__FILE__), 'config.yml'))
end

configuration = load_configuration
registry = configuration['registry']
repository = configuration['repository']
images = configuration['images']
version = configuration['version']
moquerVersion = configuration['moquerVersion']
soapUIImage= configuration['soapUIImage']
soapUIVersion= configuration['soapUIVersion']


class Docker::ImageTask
  def has_repo_tag?
    images.any? { |image| image.info['RepoTags'] && image.info['RepoTags'].include?(repo_tag) }
  end
end

def build_image(name)
  puts "  - Building image #{name}"
  {
      name: name,
      image: Docker::Image.build_from_dir(File.join(File.dirname(__FILE__), name))
  }
end

desc 'Build mocks'
image 'build_mocks' do
  puts "Pulling SoapUI image #{soapUIImage}:#{soapUIVersion}"

  unless File.directory?('./tmp_soapui')
    FileUtils.mkdir("tmp_soapui")
  end
  pwd = FileUtils.pwd()

  volumeMap = "#{pwd}/tmp_soapui:/root"
  puts "bind:  #{volumeMap}"
  puts FileUtils.cp("SoapUI_Projects/Moquer-soapui-project.xml","tmp_soapui/Moquer-soapui-project.xml")
  puts FileUtils.cp("build_moquer","tmp_soapui/build_moquer")
  image = Docker::Image.create('fromImage' => "#{soapUIImage}:#{soapUIVersion}")	
  puts "Pulled image, image id: #{image.id}"

  hostconfig = {}
  hostconfig['Binds'] = ["#{volumeMap}"]

  puts container = Docker::Container.create('Image' => image.info['RepoTags'][0], 'Volumes' => {'/root' => {}}, 'HostConfig' => hostconfig)
  
  puts container.start
  puts container.exec(['sh', '/root/build_moquer', '${endPoint}'])
  puts container.stop  
end

desc 'Build images'
image 'build' => [:build_mocks] do
  moquer_war = "tmp_soapui/moquer.war"
  FileUtils.cp(moquer_war,"moquer/moquer.war",:verbose => true) 
  puts "Building images"
  $built_images = images.map { |image| build_image(image) }
end

desc 'Tag images'
image 'tag', [:extra_tag] => [:build] do |t, args|
  puts 'Tagging images'
  $tagged_images = $built_images.map do |image|
    repo = "#{registry}/#{repository}/#{image[:name]}"

    puts "  - tagging #{repo}:#{version}"
    image[:image].tag(repo: repo, tag: version, force: true)
    if args[:extra_tag]
      puts "  - tagging #{repo}:#{args[:extra_tag]}"
      image[:image].tag(repo: repo, tag: args[:extra_tag], force: true)
    end
    image[:image]
  end
end

desc 'Push images'
image 'push' => [:tag] do
  puts 'Pushing images'
  Docker.authenticate!(username: ENV['DOCKER_REGISTRY_USER'], password: ENV['DOCKER_REGISTRY_PASSWORD'], serveraddress: 'docker.appdirect.tools') if ENV['DOCKER_REGISTRY_USER']

  $tagged_images.each do |image|
    image.info["RepoTags"].each { |tag|
	puts "  - pushing #{tag}"
	image.push(nil, repo_tag: tag)
    }
  end
end
